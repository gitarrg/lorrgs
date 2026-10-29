"""Stacks: `lorrgs-layers` (Lambda layers) and `lorrgs` (serves every Game Version, ADR 0003).

Cloudflare -> CloudFront -> API Gateway -> lorrgs-api -> SQS -> lorrgs-sqs
                                          EventBridge Scheduler -> SQS (every 6h, per Game Version)
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
    aws_s3 as s3,
    aws_scheduler as scheduler,
    aws_sqs as sqs,
)

# IMPORT LOCAL LIBRARIES
from infra import assets
from lorgs.data import GAME_VERSIONS
from lorgs.models.raid_zone import AUTO_DIFFICULTY


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

# Existing cert for lorrgs.io and *.lorrgs.io. CloudFront requires it to live in us-east-1.
API_CERTIFICATE_ARN = os.getenv("API_CERTIFICATE_ARN", "")


class SharedStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        def layer(name: str, code: lambda_.Code) -> lambda_.LayerVersion:
            return lambda_.LayerVersion(
                self,
                name,
                layer_version_name=f"lorrgs-layers-{name}",
                code=code,
                compatible_runtimes=[lambda_.Runtime.PYTHON_3_13],
                compatible_architectures=[lambda_.Architecture.ARM_64],
            )

        self.layers = [
            layer("requirements", assets.requirements_layer()),
            layer("core", assets.package_layer("lorgs")),
        ]


REFRESH_INTERVAL_HOURS = 6


def refresh_cron(hour_offset: int) -> str:
    """Every 6h, `hour_offset` hours past 0/6/12/18 (Europe/London)."""
    if not 0 <= hour_offset < REFRESH_INTERVAL_HOURS:
        raise ValueError(f"hour_offset must be in [0, {REFRESH_INTERVAL_HOURS}): {hour_offset}")
    hours = ",".join(str(h + hour_offset) for h in range(0, 24, REFRESH_INTERVAL_HOURS))
    return f"cron(0 {hours} * * ? *)"


class RefreshSchedule(typing.NamedTuple):
    """The 6h ranking refresh of one Game Version."""

    hour_offset: int
    enabled: bool = False


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
        layers: list[lambda_.ILayerVersion],
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.layers = layers
        self.certificate = acm.Certificate.from_certificate_arn(
            self,
            "api-certificate",
            API_CERTIFICATE_ARN or "",
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
            event_sources.SqsEventSource(main_queue, batch_size=5, max_concurrency=2, report_batch_item_failures=True),
        )
        sqs_fn.add_event_source(event_sources.SqsEventSource(user_queue, batch_size=1, report_batch_item_failures=True))

        role = self.schedule_role(main_queue)
        for name, refresh in schedules.items():
            self.schedule(main_queue, role, GAME_VERSIONS[name], refresh_cron(refresh.hour_offset), refresh.enabled)

        # API
        http_api = apigw.HttpApi(
            self,
            "http-api",
            api_name=self.name("api"),
            default_integration=apigw_integrations.HttpLambdaIntegration(
                id="api-integration",
                handler=api_fn,  # ty: ignore[invalid-argument-type]
            ),
        )
        distribution = self.distribution(http_api)

        cdk.CfnOutput(self, "DistributionDomain", value=distribution.distribution_domain_name)

    def name(self, name: str) -> str:
        """eg.: lorrgs-api"""
        return f"{self.prefix}-{name}"

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

    def schedule(
        self,
        queue: sqs.Queue,
        role: iam.Role,
        game_version: GameVersion,
        cron: str,
        enabled: bool,
    ) -> None:
        """Rankings refresh of one Game Version."""
        payload = {
            "task": "load_spec_rankings",
            "game_version": game_version.name,
            "spec_slug": "all",
            "boss_slug": "all",
            "difficulty": AUTO_DIFFICULTY,
            "metric": "all",
            "limit": 50,
            "clear": False,
        }
        scheduler.CfnSchedule(
            self,
            f"schedule-{game_version.name}",
            name=self.name(f"load_spec_rankings-{game_version.name}"),
            state="ENABLED" if enabled else "DISABLED",
            schedule_expression=cron,
            schedule_expression_timezone="Europe/London",
            flexible_time_window={"mode": "FLEXIBLE", "maximumWindowInMinutes": 15},
            target={
                "arn": queue.queue_arn,
                "roleArn": role.role_arn,
                "input": json.dumps(payload),
                "sqsParameters": {"messageGroupId": f"{game_version.name}-load_spec_rankings"},
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
