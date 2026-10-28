"""Stacks: `lorrgs-shared` (layers) and one `lorrgs-<version>` per Game Version.

Cloudflare -> CloudFront -> API Gateway -> lorrgs-<version>-api -> SQS -> lorrgs-<version>-sqs
                                          EventBridge Scheduler -> SQS (every 6h)
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
from lorgs.game_version import GAME_VERSIONS, RETAIL


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


class SharedStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        def layer(name: str, code: lambda_.Code) -> lambda_.LayerVersion:
            return lambda_.LayerVersion(
                self,
                name,
                layer_version_name=f"lorrgs-shared-{name}",
                code=code,
                compatible_runtimes=[lambda_.Runtime.PYTHON_3_13],
                compatible_architectures=[lambda_.Architecture.ARM_64],
            )

        self.layers = [
            layer("requirements", assets.requirements_layer()),
            layer("core", assets.package_layer("lorgs")),
        ]


class GameVersionStack(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        game_version: GameVersion,
        layers: list[lambda_.ILayerVersion],
        schedule_enabled: bool,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.gv = game_version
        self.layers = layers

        # SQS
        main_queue = self.queue("main")
        user_queue = self.queue("user-reports")

        # Lambdas
        self.lambda_env = {
            "LORRGS_GAME_VERSION": self.gv.name,
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
            bucket.grant_read_write(fn, f"{self.gv.s3_prefix}*")
            for table in tables:
                table.grant_read_write_data(fn)

        sqs_fn.add_event_source(
            event_sources.SqsEventSource(main_queue, batch_size=5, max_concurrency=2, report_batch_item_failures=True)
        )
        sqs_fn.add_event_source(event_sources.SqsEventSource(user_queue, batch_size=1, report_batch_item_failures=True))

        self.schedule(main_queue, enabled=schedule_enabled)

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
        """eg.: lorrgs-mists-api"""
        return f"lorrgs-{self.gv.name}-{name}"

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

    def schedule(self, queue: sqs.Queue, enabled: bool) -> None:
        """Rankings refresh every 6h."""
        role = iam.Role(
            self,
            "schedule-role",
            assumed_by=iam.ServicePrincipal("scheduler.amazonaws.com"),  # ty: ignore[invalid-argument-type]
        )
        queue.grant_send_messages(role)

        payload = {
            "task": "load_spec_rankings",
            "spec_slug": "all",
            "boss_slug": "all",
            "difficulty": self.gv.default_difficulty_name,
            "metric": "all",
            "limit": 50,
            "clear": False,
        }
        scheduler.CfnSchedule(
            self,
            "schedule",
            name=self.name("load_spec_rankings"),
            state="ENABLED" if enabled else "DISABLED",
            schedule_expression="cron(0 */6 * * ? *)",
            schedule_expression_timezone="Europe/London",
            flexible_time_window={"mode": "FLEXIBLE", "maximumWindowInMinutes": 15},
            target={
                "arn": queue.queue_arn,
                "roleArn": role.role_arn,
                "input": json.dumps(payload),
                "sqsParameters": {"messageGroupId": "load_spec_rankings"},
                "retryPolicy": {"maximumEventAgeInSeconds": 86400, "maximumRetryAttempts": 0},
            },
        )

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
            price_class=cloudfront.PriceClass.PRICE_CLASS_100,
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.HttpOrigin(f"{http_api.http_api_id}.execute-api.{self.region}.amazonaws.com"),
                allowed_methods=cloudfront.AllowedMethods.ALLOW_ALL,
                cache_policy=cache_policy,
                origin_request_policy=cloudfront.OriginRequestPolicy.ALL_VIEWER_EXCEPT_HOST_HEADER,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
        )
