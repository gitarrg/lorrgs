#!/usr/bin/env -S PYTHONPATH=. uv run
"""Create the AWS resources for a Game Version from the fixed config below.

Dry run by default: it only checks whether the new resources already exist and prints what it would create.
Pass `--apply` to actually create anything. Existing resources are left alone, so it can be re-run.

    scripts/setup_game_version.py forever
    scripts/setup_game_version.py forever --apply

Creates (names are `lorrgs-<game version>-<name>`):
    - the FIFO queues `lorrgs-<version>-main.fifo` and `lorrgs-<version>-user-reports.fifo`
    - the Lambdas `lorrgs-<version>-api` and `lorrgs-<version>-sqs` (placeholder code; `scripts/deploy.py`
      replaces it), and the SQS triggers
    - a public Function URL for the API Lambda
    - the ranking refresh schedule, DISABLED (there is nothing to refresh before the Game Version has a raid)

The Lambda environment gets `LORRGS_GAME_VERSION` and the queue urls. Credentials
(`WCL_*`, `DISCORD_*`, `REDIS_URL`, `SECRET_KEY`, `MONGO_URI`) are not copied from anywhere; set them
on the new Lambdas before they can load reports.

Not covered (manual): the DNS record for `<game version>-api.lorrgs.io` (Cloudflare) and enabling the
schedule. `REFRESH_SCHEDULE["RoleArn"]` is the Retail scheduler role. Its trust policy lets any
EventBridge schedule in this account assume it, and its policy allows `sqs:SendMessage` to any queue
in the account.

Infrastructure as code (#89) is meant to replace this script.
"""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import argparse
import io
import json
import typing
import zipfile

# IMPORT THIRD-PARTY LIBRARIES
import boto3
from botocore.exceptions import ClientError

# IMPORT LOCAL LIBRARIES
from lorgs.game_version import GAME_VERSIONS, RETAIL


PROJECT_NAME = "lorrgs"


class QueueAttributes(typing.TypedDict):
    FifoQueue: str
    ContentBasedDeduplication: str
    DeduplicationScope: str
    FifoThroughputLimit: str
    VisibilityTimeout: str
    MessageRetentionPeriod: str
    SqsManagedSseEnabled: str


class LambdaConfig(typing.TypedDict):
    Role: str
    Handler: str
    Timeout: int


class FlexibleWindow(typing.TypedDict):
    Mode: typing.Literal["FLEXIBLE"]
    MaximumWindowInMinutes: int


class RetryPolicy(typing.TypedDict):
    MaximumEventAgeInSeconds: int
    MaximumRetryAttempts: int


class RefreshSchedule(typing.TypedDict):
    ScheduleExpression: str
    ScheduleExpressionTimezone: str
    FlexibleTimeWindow: FlexibleWindow
    RoleArn: str
    RetryPolicy: RetryPolicy
    MessageGroupId: str


# Both queues. Values are strings because that is what `create_queue` takes.
QUEUE_ATTRIBUTES: QueueAttributes = {
    "FifoQueue": "true",
    "ContentBasedDeduplication": "true",
    "DeduplicationScope": "messageGroup",
    "FifoThroughputLimit": "perMessageGroupId",
    "VisibilityTimeout": "180",
    "MessageRetentionPeriod": "86400",  # 1 day
    "SqsManagedSseEnabled": "true",
}

# Shared by both Lambdas. `scripts/deploy.py` updates the layers when they change.
LAMBDA_RUNTIME = "python3.13"
LAMBDA_MEMORY = 512
LAMBDA_ARCHITECTURES: list[typing.Literal["arm64"]] = ["arm64"]
LAMBDA_LAYERS = [
    "arn:aws:lambda:eu-west-1:746912274922:layer:lorrgs-requirements:17",
    "arn:aws:lambda:eu-west-1:746912274922:layer:lorrgs-core:297",
]
LAMBDA_CONFIG: dict[str, LambdaConfig] = {
    "api": {
        "Role": "arn:aws:iam::746912274922:role/service-role/lorrgs-api-lambda-role",
        "Handler": "lorrgs_api.handler.handler",
        "Timeout": 30,
    },
    "sqs": {
        "Role": "arn:aws:iam::746912274922:role/service-role/lorrgs-sqs-role-npr2706c",
        "Handler": "lorrgs_sqs.handler.handler",
        "Timeout": 180,
    },
}


# SQS trigger on `lorrgs-<version>-sqs`, keyed by the queue's short name.
TRIGGER_CONFIG = {
    "main.fifo": {
        "BatchSize": 5,
        "ScalingConfig": {"MaximumConcurrency": 2},
        "FunctionResponseTypes": ["ReportBatchItemFailures"],
    },
    "user-reports.fifo": {
        "BatchSize": 1,
        "FunctionResponseTypes": ["ReportBatchItemFailures"],
    },
}

# Rankings refresh every 6h. Created DISABLED.
REFRESH_SCHEDULE: RefreshSchedule = {
    "ScheduleExpression": "cron(0 */6 * * ? *)",
    "ScheduleExpressionTimezone": "Europe/London",
    "FlexibleTimeWindow": {
        "Mode": "FLEXIBLE",
        "MaximumWindowInMinutes": 15,
    },
    "RoleArn": "arn:aws:iam::746912274922:role/service-role/Amazon_EventBridge_Scheduler_SQS_8ac2cf814f",
    "RetryPolicy": {
        "MaximumEventAgeInSeconds": 86400,
        "MaximumRetryAttempts": 0,
    },
    "MessageGroupId": "load_spec_rankings",
}

LAMBDA = boto3.client("lambda")
SQS = boto3.client("sqs")
SCHEDULER = boto3.client("scheduler")


def _missing(exc: ClientError) -> bool:
    code = exc.response.get("Error", {}).get("Code", "")
    return code in {"AWS.SimpleQueueService.NonExistentQueue", "QueueDoesNotExist", "ResourceNotFoundException"}


def placeholder_zip() -> bytes:
    """Stand-in code so the function can be created. `scripts/deploy.py` replaces it."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for package in ("lorrgs_api", "lorrgs_sqs"):
            archive.writestr(f"{package}/__init__.py", "")
            archive.writestr(
                f"{package}/handler.py",
                "def handler(event, context):\n"
                "    raise RuntimeError('run scripts/deploy.py to deploy the code')\n",
            )
    return buffer.getvalue()


class Setup:
    def __init__(self, game_version_name: str, apply: bool) -> None:  # ruff: ignore[boolean-type-hint-positional-argument]
        self.gv = GAME_VERSIONS[game_version_name]
        self.apply = apply

    def name(self, name: str) -> str:
        """The resource's full name, eg.: lorrgs-mists-api."""
        return f"{PROJECT_NAME}-{self.gv.name}-{name}"

    def log(self, message: str) -> None:
        print(f"{'' if self.apply else '[dry run] '}{message}")

    ############################################################################
    # SQS

    def queue(self, name: str) -> str:
        """Create the queue and return its url (a placeholder on a dry run)."""
        new_name = self.name(name)
        try:
            return SQS.get_queue_url(QueueName=new_name)["QueueUrl"]
        except ClientError as exc:
            if not _missing(exc):
                raise

        self.log(f"create queue {new_name}")
        if not self.apply:
            return f"<url of {new_name}>"
        return SQS.create_queue(
            QueueName=new_name,
            Attributes=QUEUE_ATTRIBUTES,  # ty: ignore[invalid-argument-type]
        )["QueueUrl"]

    ############################################################################
    # Lambda

    def function(self, name: str, queue_env: dict[str, str]) -> str:
        """Create the Lambda and return its arn."""
        new_name = self.name(name)
        try:
            return LAMBDA.get_function_configuration(FunctionName=new_name)["FunctionArn"]
        except LAMBDA.exceptions.ResourceNotFoundException:
            pass

        config = LAMBDA_CONFIG[name]
        variables = {
            **queue_env,
            "LORRGS_GAME_VERSION": self.gv.name,
        }
        self.log(f"create lambda {new_name} (LORRGS_GAME_VERSION={self.gv.name})")
        if not self.apply:
            return f"<arn of {new_name}>"

        response = LAMBDA.create_function(
            FunctionName=new_name,
            Runtime=LAMBDA_RUNTIME,
            Role=config["Role"],
            Handler=config["Handler"],
            Code={"ZipFile": placeholder_zip()},
            Timeout=config["Timeout"],
            MemorySize=LAMBDA_MEMORY,
            Architectures=LAMBDA_ARCHITECTURES,
            Layers=LAMBDA_LAYERS,
            Environment={"Variables": variables},
        )
        LAMBDA.get_waiter("function_active_v2").wait(FunctionName=new_name)
        return response["FunctionArn"]

    def trigger(self, queue_name: str) -> None:
        """Wire the queue to the SQS Lambda."""
        new_queue_name = self.name(queue_name)
        new_function = self.name("sqs")
        config = TRIGGER_CONFIG[queue_name]

        if not self.apply:
            self.log(f"trigger {new_function} from {new_queue_name} (batch size {config['BatchSize']})")
            return

        queue_arn = SQS.get_queue_attributes(
            QueueUrl=SQS.get_queue_url(QueueName=new_queue_name)["QueueUrl"],
            AttributeNames=["QueueArn"],
        )["Attributes"]["QueueArn"]
        mappings = LAMBDA.list_event_source_mappings(FunctionName=new_function, EventSourceArn=queue_arn)
        if mappings["EventSourceMappings"]:
            return
        LAMBDA.create_event_source_mapping(
            FunctionName=new_function,
            EventSourceArn=queue_arn,
            **config,  # ty: ignore[invalid-argument-type]
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
        """Rankings refresh every 6h, DISABLED until there is a raid to refresh."""
        name = self.name("load_spec_rankings")
        try:
            SCHEDULER.get_schedule(Name=name)
        except SCHEDULER.exceptions.ResourceNotFoundException:
            pass
        else:
            return

        payload = {
            "task": "load_spec_rankings",
            "spec_slug": "all",
            "boss_slug": "all",
            "difficulty": self.gv.default_difficulty_name,
            "metric": "all",
            "limit": 50,
            "clear": False,
        }
        self.log(f"create schedule {name} ({REFRESH_SCHEDULE['ScheduleExpression']}, DISABLED)")
        if not self.apply:
            return

        queue_arn = SQS.get_queue_attributes(QueueUrl=queue_url, AttributeNames=["QueueArn"])["Attributes"]["QueueArn"]
        SCHEDULER.create_schedule(
            Name=name,
            State="DISABLED",
            ScheduleExpression=REFRESH_SCHEDULE["ScheduleExpression"],
            ScheduleExpressionTimezone=REFRESH_SCHEDULE["ScheduleExpressionTimezone"],
            FlexibleTimeWindow=REFRESH_SCHEDULE["FlexibleTimeWindow"],  # ty: ignore[invalid-argument-type]
            Target={  # ty: ignore[invalid-argument-type]
                "Arn": queue_arn,
                "RoleArn": REFRESH_SCHEDULE["RoleArn"],
                "RetryPolicy": REFRESH_SCHEDULE["RetryPolicy"],
                "Input": json.dumps(payload),
                "SqsParameters": {"MessageGroupId": REFRESH_SCHEDULE["MessageGroupId"]},
            },
        )


def main() -> None:

    ###########################
    # ARGPARSE
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("game_version", choices=[gv.name for gv in GAME_VERSIONS.values() if gv is not RETAIL])
    parser.add_argument("--apply", action="store_true", help="create the resources (default: dry run)")
    args = parser.parse_args()

    ###########################
    # init
    setup = Setup(args.game_version, apply=args.apply)

    ###########################
    # sqs
    main_queue = setup.queue("main.fifo")
    user_queue = setup.queue("user-reports.fifo")

    ###########################
    # lambda
    queue_env = {"SQS_QUEUE_URL": main_queue, "SQS_USER_QUEUE_URL": user_queue}
    setup.function("api", queue_env)
    setup.function("sqs", queue_env)
    setup.trigger("main.fifo")
    setup.trigger("user-reports.fifo")
    setup.function_url("api")
    setup.refresh_schedule(main_queue)

    if not args.apply:
        print("\nDry run only. Re-run with --apply to create these.")


if __name__ == "__main__":
    main()
