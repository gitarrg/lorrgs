#!/usr/bin/env -S PYTHONPATH=. uv run
"""Create the AWS resources for a Game Version by cloning the Retail ones.

Dry run by default: it only reads from AWS and prints what it would create.
Pass `--apply` to actually create anything. Existing resources are left alone, so it can be re-run.

    scripts/setup_game_version.py forever
    scripts/setup_game_version.py forever --apply

Creates (all names carry `GameVersion.deploy_prefix`):
    - the FIFO queues `<prefix>lorrgs-main.fifo` and `<prefix>lorrgs-user-reports.fifo`
    - the Lambdas `<prefix>lorrgs-api` and `<prefix>lorrgs-sqs` (config and layers copied from Retail,
      with `LORRGS_GAME_VERSION` and the queue urls overridden), and the SQS triggers
    - a public Function URL for the API Lambda
    - the ranking refresh schedule, DISABLED (there is nothing to refresh before the Game Version has a raid)

Not covered (manual): the DNS record for `<game version>-api.lorrgs.io` (Cloudflare), IAM permissions for the
copied roles to reach the new queues, and enabling the schedule. `scripts/deploy.py` deploys the code afterwards.

Infrastructure as code (#89) is meant to replace this script.
"""

import argparse
import json
import os

import boto3

from lorgs.game_version import GAME_VERSIONS, RETAIL, GameVersion


DEPLOY_BUCKET = os.getenv("DEPLOY_BUCKET") or "lorrgs-code"

LAMBDA = boto3.client("lambda")
SQS = boto3.client("sqs")
S3 = boto3.client("s3")
SCHEDULER = boto3.client("scheduler")

# queue attributes we copy from the Retail queues (the rest is account/queue specific)
QUEUE_ATTRIBUTES = [
    "FifoQueue",
    "ContentBasedDeduplication",
    "DeduplicationScope",
    "FifoThroughputLimit",
    "VisibilityTimeout",
    "MessageRetentionPeriod",
    "SqsManagedSseEnabled",
]


class Setup:
    def __init__(self, game_version: GameVersion, apply: bool) -> None:
        self.gv = game_version
        self.apply = apply

    def name(self, name: str) -> str:
        return f"{self.gv.deploy_prefix}{name}"

    def log(self, message: str) -> None:
        print(f"{'' if self.apply else '[dry run] '}{message}")

    ############################################################################
    # SQS

    def queue(self, name: str) -> str:
        """Create the queue (cloned from Retail's) and return its url (a placeholder on a dry run)."""
        new_name = self.name(name)
        try:
            return SQS.get_queue_url(QueueName=new_name)["QueueUrl"]
        except SQS.exceptions.QueueDoesNotExist:
            pass

        source_url = SQS.get_queue_url(QueueName=name)["QueueUrl"]
        attributes = SQS.get_queue_attributes(QueueUrl=source_url, AttributeNames=QUEUE_ATTRIBUTES)["Attributes"]
        self.log(f"create queue {new_name}")
        if not self.apply:
            return f"<url of {new_name}>"
        return SQS.create_queue(QueueName=new_name, Attributes=attributes)["QueueUrl"]

    ############################################################################
    # Lambda

    def function(self, name: str, env: dict[str, str]) -> str:
        """Create the Lambda (cloned from Retail's) and return its arn."""
        new_name = self.name(name)
        try:
            return LAMBDA.get_function_configuration(FunctionName=new_name)["FunctionArn"]
        except LAMBDA.exceptions.ResourceNotFoundException:
            pass

        source = LAMBDA.get_function_configuration(FunctionName=name)
        variables = {**source["Environment"]["Variables"], **env, "LORRGS_GAME_VERSION": self.gv.name}
        self.log(f"create lambda {new_name} (env: {', '.join(sorted(env))}, LORRGS_GAME_VERSION={self.gv.name})")
        if not self.apply:
            return f"<arn of {new_name}>"

        # start from Retail's current code; deploy.py replaces it with the real one
        S3.copy_object(
            Bucket=DEPLOY_BUCKET,
            Key=f"{new_name}.zip",
            CopySource={"Bucket": DEPLOY_BUCKET, "Key": f"{name}.zip"},
        )
        response = LAMBDA.create_function(
            FunctionName=new_name,
            Runtime=source["Runtime"],
            Role=source["Role"],
            Handler=source["Handler"],
            Code={"S3Bucket": DEPLOY_BUCKET, "S3Key": f"{new_name}.zip"},
            Timeout=source["Timeout"],
            MemorySize=source["MemorySize"],
            Architectures=source["Architectures"],
            Layers=[layer["Arn"] for layer in source.get("Layers", [])],
            Environment={"Variables": variables},
        )
        LAMBDA.get_waiter("function_active_v2").wait(FunctionName=new_name)
        return response["FunctionArn"]

    def trigger(self, function_name: str, source_name: str, queue_name: str) -> None:
        """Wire the queue to the Lambda, with the batch settings of the Retail trigger."""
        new_queue_name = self.name(queue_name)
        new_function = self.name(function_name)

        source_arn = SQS.get_queue_attributes(
            QueueUrl=SQS.get_queue_url(QueueName=queue_name)["QueueUrl"], AttributeNames=["QueueArn"]
        )["Attributes"]["QueueArn"]
        (source,) = LAMBDA.list_event_source_mappings(FunctionName=source_name, EventSourceArn=source_arn)[
            "EventSourceMappings"
        ]

        if not self.apply:
            self.log(f"trigger {new_function} from {new_queue_name} (batch size {source['BatchSize']})")
            return

        queue_arn = SQS.get_queue_attributes(
            QueueUrl=SQS.get_queue_url(QueueName=new_queue_name)["QueueUrl"], AttributeNames=["QueueArn"]
        )["Attributes"]["QueueArn"]
        if LAMBDA.list_event_source_mappings(FunctionName=new_function, EventSourceArn=queue_arn)["EventSourceMappings"]:
            return
        kwargs = {}
        if "ScalingConfig" in source:
            kwargs["ScalingConfig"] = source["ScalingConfig"]
        LAMBDA.create_event_source_mapping(
            FunctionName=new_function, EventSourceArn=queue_arn, BatchSize=source["BatchSize"], **kwargs
        )
        print(f"trigger {new_function} from {new_queue_name}")

    def function_url(self, name: str) -> None:
        new_name = self.name(name)
        try:
            url = LAMBDA.get_function_url_config(FunctionName=new_name)["FunctionUrl"]
        except LAMBDA.exceptions.ResourceNotFoundException:
            self.log(f"create function url for {new_name}")
            if not self.apply:
                return
            # CORS is handled by the app's own middleware, not by the Function URL
            url = LAMBDA.create_function_url_config(FunctionName=new_name, AuthType="NONE")["FunctionUrl"]
            LAMBDA.add_permission(
                FunctionName=new_name,
                StatementId="FunctionURLAllowPublicAccess",
                Action="lambda:InvokeFunctionUrl",
                Principal="*",
                FunctionUrlAuthType="NONE",
            )
        print(f"function url of {new_name}: {url}  (point {self.gv.name}-api.lorrgs.io at it)")

    ############################################################################
    # Scheduler

    def refresh_schedule(self, queue_url: str) -> None:
        """Rankings refresh every 6h, like Retail's, but DISABLED until there is a raid to refresh."""
        name = self.name("lorrgs.load_spec_rankings")
        source = SCHEDULER.get_schedule(Name=f"lorrgs.load_spec_rankings.{RETAIL.default_difficulty_name}")
        try:
            SCHEDULER.get_schedule(Name=name)
            return
        except SCHEDULER.exceptions.ResourceNotFoundException:
            pass

        payload = {
            "task": "load_spec_rankings",
            "spec_slug": "all",
            "boss_slug": "all",
            "difficulty": self.gv.default_difficulty_name,
            "metric": "all",
            "limit": 50,
            "clear": False,
        }
        self.log(f"create schedule {name} ({source['ScheduleExpression']}, DISABLED)")
        if not self.apply:
            return

        queue_arn = SQS.get_queue_attributes(QueueUrl=queue_url, AttributeNames=["QueueArn"])["Attributes"]["QueueArn"]
        target = {
            **{key: source["Target"][key] for key in ("RoleArn", "RetryPolicy")},
            "Arn": queue_arn,
            "Input": json.dumps(payload),
            "SqsParameters": {"MessageGroupId": "load_spec_rankings"},
        }
        SCHEDULER.create_schedule(
            Name=name,
            State="DISABLED",
            ScheduleExpression=source["ScheduleExpression"],
            ScheduleExpressionTimezone=source["ScheduleExpressionTimezone"],
            FlexibleTimeWindow=source["FlexibleTimeWindow"],
            Target=target,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("game_version", choices=[gv.name for gv in GAME_VERSIONS.values() if gv is not RETAIL])
    parser.add_argument("--apply", action="store_true", help="create the resources (default: dry run)")
    args = parser.parse_args()

    setup = Setup(GAME_VERSIONS[args.game_version], apply=args.apply)

    main_queue = setup.queue("lorrgs-main.fifo")
    user_queue = setup.queue("lorrgs-user-reports.fifo")

    env = {"SQS_QUEUE_URL": main_queue, "SQS_USER_QUEUE_URL": user_queue}
    setup.function("lorrgs-api", env)
    setup.function("lorrgs-sqs", env)
    setup.trigger("lorrgs-sqs", source_name="lorrgs-sqs", queue_name="lorrgs-main.fifo")
    setup.trigger("lorrgs-sqs", source_name="lorrgs-sqs", queue_name="lorrgs-user-reports.fifo")
    setup.function_url("lorrgs-api")
    setup.refresh_schedule(main_queue)

    if not args.apply:
        print("\nDry run only. Re-run with --apply to create these.")


if __name__ == "__main__":
    main()
