"""Stack `lorrgs`: serves every Game Version (ADR 0003).

Cloudflare -> CloudFront -> API Gateway -> lorrgs-api -> SQS -> lorrgs-sqs
                                          EventBridge Scheduler -> SQS (hourly planner; daily Builds per Game Version)

Lambda layers live here. A layer version is immutable, so a code change replaces
it. CloudFormation can replace it in the same stack as the functions that import
the layer ARN: new version, repoint the functions, then delete the old version.
"""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import json
import os
import typing

# IMPORT THIRD-PARTY LIBRARIES
import aws_cdk as cdk
from aws_cdk import (
    aws_apigatewayv2 as apigw,
    aws_apigatewayv2_integrations as apigw_integrations,
    aws_certificatemanager as acm,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_lambda_event_sources as event_sources,
    aws_logs as logs,
    aws_s3 as s3,
    aws_scheduler as scheduler,
    aws_sqs as sqs,
)

# IMPORT LOCAL LIBRARIES
from infra import assets
from lorgs.data import GAME_VERSIONS


if typing.TYPE_CHECKING:
    from constructs import Construct

    from lorgs.models.game_version import GameVersion


SECRETS = (
    "WCL_CLIENT_ID",
    "WCL_CLIENT_SECRET",
    "WCL_AUTH_TOKEN",
    "DISCORD_CLIENT_ID",
    "DISCORD_CLIENT_SECRET",
    "DISCORD_BOT_TOKEN",
    "DISCORD_WEBHOOK_URL",
    "REDIS_URL",
    "SECRET_KEY",
)
"""Copied from the deploying environment (`.env` locally) onto the Lambdas."""

SPEC_RANKING_VIEWS_QUERY = """filter @message like "spec_ranking_view"
| parse @message "game_version=* spec=* boss=* difficulty=* metric=* default_metric=*" as gv, spec, boss, difficulty, metric, is_default
| stats count() as views by gv, metric, is_default, bin(1d) as day
| sort day desc, gv, views desc"""
"""Logs Insights: Spec Ranking views per Game Version, metric and day (#130). Counts cache misses only."""

# Existing cert for lorrgs.io and *.lorrgs.io. CloudFront requires it to live in us-east-1.
# Read at stack construction, after `dotenv.load_dotenv()` in infra/app.py.


REFRESH_INTERVAL_HOURS = 6


PLANNER_CRON = "cron(1 * * * ? *)"
"""Minute 1 of every hour: Warcraft Logs resets the points on the hour."""


def builds_cron(hour_offset: int) -> str:
    """Daily at 03:30 (Europe/London), `hour_offset` hours later: after the hourly Refresh Planner has had time to refresh the rankings."""
    if not 0 <= hour_offset < REFRESH_INTERVAL_HOURS:
        raise ValueError(f"hour_offset must be in [0, {REFRESH_INTERVAL_HOURS}): {hour_offset}")
    return f"cron(30 {3 + hour_offset} * * ? *)"


class RefreshSchedule(typing.NamedTuple):
    """Whether the hourly Refresh Planner covers one Game Version, and its daily Builds refresh (Game Versions with talents only).

    `hour_offset` only places the Builds refresh. The planner schedule is enabled while any Game Version is.
    """

    hour_offset: int
    enabled: bool = False
    builds_enabled: bool = False


class LorrgsStack(cdk.Stack):
    """Queues, Lambdas, schedules, API Gateway and CloudFront serving every Game Version on `api.lorrgs.io`."""

    prefix = "lorrgs"
    domain = "api.lorrgs.io"

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        schedules: dict[str, RefreshSchedule],
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.layers = [
            self.layer("requirements", assets.requirements_layer()),
            self.layer("core", assets.package_layer("lorgs")),
        ]
        self.certificate = acm.Certificate.from_certificate_arn(
            self,
            "api-certificate",
            os.getenv("API_CERTIFICATE_ARN", ""),
        )

        # SQS
        main_queue = self.queue("main")
        user_queue = self.queue("user-reports")

        # Lambdas
        self.lambda_env = {
            "SQS_QUEUE_URL": main_queue.queue_url,
            "SQS_USER_QUEUE_URL": user_queue.queue_url,
            **{name: os.getenv(name, "") for name in SECRETS},
        }
        api_fn = self.function("api", "lorrgs_api", timeout=30)  # API Gateway's limit
        sqs_fn = self.function("sqs", "lorrgs_sqs", timeout=180)

        bucket = s3.Bucket.from_bucket_name(self, "data", "lorrgs")
        tables = [dynamodb.Table.from_table_name(self, name, name) for name in ("user", "user_report")]
        for fn in (api_fn, sqs_fn):
            main_queue.grant_send_messages(fn)
            user_queue.grant_send_messages(fn)
            for version in GAME_VERSIONS.values():
                bucket.grant_read_write(fn, f"{version.s3_prefix}*")
            for table in tables:
                table.grant_read_write_data(fn)

        sqs_fn.add_event_source(
            event_sources.SqsEventSource(
                main_queue,
                batch_size=5,
                max_concurrency=2,
                report_batch_item_failures=True,
            ),
        )
        sqs_fn.add_event_source(
            event_sources.SqsEventSource(
                user_queue,
                batch_size=1,
                report_batch_item_failures=True,
            ),
        )

        role = self.schedule_role(main_queue)
        self.planner_schedule(main_queue, role, enabled=any(refresh.enabled for refresh in schedules.values()))
        for name, refresh in schedules.items():
            if GAME_VERSIONS[name].has_talents:
                self.builds_schedule(
                    main_queue,
                    role,
                    GAME_VERSIONS[name],
                    builds_cron(refresh.hour_offset),
                    enabled=refresh.builds_enabled,
                )

        # API
        http_api = apigw.HttpApi(
            self,
            "http-api",
            api_name=self.name("api"),
            default_integration=apigw_integrations.HttpLambdaIntegration(
                id="api-integration",
                handler=api_fn,
            ),
        )
        distribution = self.distribution(http_api)

        logs.CfnQueryDefinition(
            self,
            "spec-ranking-views",
            name=f"{self.prefix}/spec-ranking-views",
            query_string=SPEC_RANKING_VIEWS_QUERY,
            log_group_names=[f"/aws/lambda/{api_fn.function_name}"],
        )

        cdk.CfnOutput(self, "DistributionDomain", value=distribution.distribution_domain_name)

    def name(self, name: str) -> str:
        """eg.: lorrgs-api."""
        return f"{self.prefix}-{name}"

    def layer(self, name: str, code: lambda_.Code) -> lambda_.LayerVersion:
        return lambda_.LayerVersion(
            self,
            f"layer-{name}",
            layer_version_name=f"lorrgs-layers-{name}",
            code=code,
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_13],
            compatible_architectures=[lambda_.Architecture.ARM_64],
        )

    def queue(self, name: str) -> sqs.Queue:
        return sqs.Queue(
            self,
            name,
            queue_name=self.name(f"{name}.fifo"),
            fifo=True,
            content_based_deduplication=True,
            deduplication_scope=sqs.DeduplicationScope.MESSAGE_GROUP,
            fifo_throughput_limit=sqs.FifoThroughputLimit.PER_MESSAGE_GROUP_ID,
            visibility_timeout=cdk.Duration.seconds(180),
            retention_period=cdk.Duration.days(1),
        )

    def function(self, name: str, package: str, timeout: int) -> lambda_.Function:
        return lambda_.Function(
            self,
            name,
            function_name=self.name(name),
            runtime=lambda_.Runtime.PYTHON_3_13,
            architecture=lambda_.Architecture.ARM_64,
            handler=f"{package}.handler.handler",
            code=assets.package_code(package),
            layers=self.layers,
            memory_size=512,
            timeout=cdk.Duration.seconds(timeout),
            environment=self.lambda_env,
        )

    def planner_schedule(self, queue: sqs.Queue, role: iam.Role, *, enabled: bool) -> None:
        """Hourly Refresh Planner: queues the Spec Ranking Refreshes of every Game Version with updates enabled."""
        scheduler.CfnSchedule(
            self,
            "planner-schedule",
            name=self.name("plan_spec_rankings"),
            state="ENABLED" if enabled else "DISABLED",
            schedule_expression=PLANNER_CRON,
            schedule_expression_timezone="Europe/London",
            flexible_time_window={"mode": "OFF"},
            target={
                "arn": queue.queue_arn,
                "roleArn": role.role_arn,
                "input": json.dumps({"task": "plan_spec_rankings"}),
                "sqsParameters": {"messageGroupId": "plan_spec_rankings"},
                "retryPolicy": {"maximumEventAgeInSeconds": 3600, "maximumRetryAttempts": 0},
            },
        )

    def builds_schedule(
        self,
        queue: sqs.Queue,
        role: iam.Role,
        game_version: GameVersion,
        cron: str,
        *,
        enabled: bool,
    ) -> None:
        """Daily Builds refresh of every playable spec of one Game Version."""
        payload = {"task": "load_spec_builds", "game_version": game_version.name, "spec_slug": "all"}
        scheduler.CfnSchedule(
            self,
            f"builds-schedule-{game_version.name}",
            name=self.name(f"load_spec_builds-{game_version.name}"),
            state="ENABLED" if enabled else "DISABLED",
            schedule_expression=cron,
            schedule_expression_timezone="Europe/London",
            flexible_time_window={"mode": "FLEXIBLE", "maximumWindowInMinutes": 15},
            target={
                "arn": queue.queue_arn,
                "roleArn": role.role_arn,
                "input": json.dumps(payload),
                "sqsParameters": {"messageGroupId": f"{game_version.name}-load_spec_builds"},
                "retryPolicy": {"maximumEventAgeInSeconds": 86400, "maximumRetryAttempts": 0},
            },
        )

    def schedule_role(self, queue: sqs.Queue) -> iam.Role:
        role = iam.Role(
            self,
            "schedule-role",
            assumed_by=iam.ServicePrincipal("scheduler.amazonaws.com"),  # ty: ignore[invalid-argument-type]
        )
        queue.grant_send_messages(role)
        return role

    def distribution(self, http_api: apigw.HttpApi) -> cloudfront.Distribution:
        """CloudFront in front of the API, caching by the app's `Cache-Control` headers."""
        cache_policy = cloudfront.CachePolicy(
            self,
            "cache-policy",
            cache_policy_name=self.name("api"),
            default_ttl=cdk.Duration.seconds(0),
            query_string_behavior=cloudfront.CacheQueryStringBehavior.all(),
            header_behavior=cloudfront.CacheHeaderBehavior.allow_list("Origin"),  # the app sends `Vary: Origin`
            enable_accept_encoding_gzip=True,
            enable_accept_encoding_brotli=True,
        )
        return cloudfront.Distribution(
            self,
            "distribution",
            comment=self.name("api"),
            domain_names=[self.domain],
            certificate=self.certificate,
            minimum_protocol_version=cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021,
            price_class=cloudfront.PriceClass.PRICE_CLASS_100,
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.HttpOrigin(f"{http_api.http_api_id}.execute-api.{self.region}.amazonaws.com"),
                allowed_methods=cloudfront.AllowedMethods.ALLOW_ALL,
                cache_policy=cache_policy,
                origin_request_policy=cloudfront.OriginRequestPolicy.ALL_VIEWER_EXCEPT_HOST_HEADER,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.ALLOW_ALL,  # allow HTTP and HTTPS
            ),
        )
