# AWS inventory for the cutover (#116)

Snapshot of account `746912274922` / `eu-west-1`, taken 2026-10-30 (read-only). Lists everything the `lorrgs` stack (ADR 0003) makes obsolete, and when it can go. See `docs/deploy_game_versions.md` for the rollout steps.

- **Before**: must be gone before `scripts/deploy` creates the `lorrgs` stack.
- **After**: still serves prod until the frontend uses `api.lorrgs.io`.
- **Dead**: unused today; unrelated to the cutover.

## Before the deploy

| Resource | Why |
| --- | --- |
| Lambda `lorrgs-api` | Name clash. Takes its API Gateway permissions and Function URL with it. |
| Lambda `lorrgs-sqs` | Name clash. Takes its 2 event source mappings with it. |
| SQS `lorrgs-main.fifo` | Name clash. Had 844 queued messages and a redrive policy pointing at itself: drain or inspect first. |
| SQS `lorrgs-user-reports.fifo` | Name clash. |
| Scheduler `lorrgs.load_spec_rankings.mythic` (enabled) | Targets the `lorrgs-main.fifo` ARN: once the new queue exists, it would send old payloads (no `game_version`) into it. |
| Scheduler `lorrgs.load_spec_rankings.heroic` (enabled) | Same. |
| Scheduler `lorrgs.load_comp_rankings2` (enabled) | Same. |
| EventBridge rule `lorrgs.load_spec_rankings` (disabled) | Same target. |

Deleting the two Lambdas takes `api2.lorrgs.io` down, unless they are first replaced by copies under other names (`lorrgs-legacy-*`) behind the same API Gateway.

## After the frontend switch

| Resource | Notes |
| --- | --- |
| CloudFront `E2OI55KUCSVW22` (`api2.lorrgs.io`, `aws.lorrgs.io`) | Current Retail API front, incl. the `/api/dev/spec_ranking/*` → S3 behaviour. |
| HTTP API `4igq805waf` (`lorrgs-api`) | Origin of the distribution above. |
| API Gateway custom domains `cherry.lorrgs.io`, `fish.lorrgs.io` | Both map to `4igq805waf`; likely unused already. |
| Stack `lorrgs-mists` | Lambdas, queues, schedule, API, CloudFront `E1R3WR2DE32S46` (`mists-api.lorrgs.io`), roles. |
| Stack `lorrgs-forever` | Same, CloudFront `E18VKICNGH2O9W` (`forever-api.lorrgs.io`). |
| Stack `lorrgs-shared` | Layers `lorrgs-shared-core:1`, `lorrgs-shared-requirements:1`. Delete after the two stacks above. |
| S3 `lorrgs/spec_ranking/`, `lorrgs/comp_ranking/` | Un-prefixed Retail rankings; only after the last copy to `retail/`. |
| Layers `lorrgs-core:297`, `lorrgs-requirements:17` | Used only by the old Retail Lambdas (or their copies). |
| IAM `lorrgs-api-lambda-role`, `lorrgs-sqs-role-npr2706c` | Roles of the old Retail Lambdas (or their copies). |
| IAM `Amazon_EventBridge_Scheduler_SQS_8ac2cf814f`, `…_b8e2bbefe7`, `…_921682de7b` | Roles of the 3 old schedules; can go with them. |
| Cloudflare DNS `api2`, `mists-api`, `forever-api`, `aws` | Outside AWS. |

## Dead leftovers

| Resource | Evidence |
| --- | --- |
| Lambda `lorrgs-sns`, IAM `lorrgs-sns-role-7d87jqc7`, log group `/aws/lambda/lorrgs-sns` | Only triggered by SNS `lorrgs-tasks`; nothing publishes to it. |
| SNS `lorrgs-tasks`, `lorrgs-tasks.fifo` | Not referenced in code. |
| SQS `lorrgs-errors` | Empty, no consumer, no queue's dead-letter target. |
| Function URL of `lorrgs-api` | Origin on `E2OI55KUCSVW22`, but no behaviour routes to it. |
| DynamoDB `task` | 0 items; Tasks live in Redis. |
| IAM `lorrgs-stats-role-23kjgdtq`, log group `/aws/lambda/lorrgs-stats` | No `lorrgs-stats` Lambda exists. |
| IAM `lorrgs-error-handler-role-jrujd1tb`, `test-lorrgs-api-role`, `lorrgs-mists-load_spec_rankings` | Unattached. |
| IAM `Amazon_EventBridge_Scheduler_SQS_5e30541231`, `…_SQS_eb3eaa7906`, `…_LAMBDA_c9d9fbcb1b`, `…_LAMBDA_e2a98309ef` | No schedule uses them. |
| Layers `dev--lorrgs-core`, `dev--lorrgs-requirements` | No function uses them. |
| WebSocket API `ws-test` (`zft6ckjdzh`) | Experiment. |
| CloudFront `E3AQF4NDGUP3P6` ("Test", S3 origin, no alias) | Experiment. |

## Keep

- S3 bucket `lorrgs` (incl. `retail/`, `mists/`), DynamoDB `user` and `user_report`.
- Log groups `/aws/lambda/lorrgs-api` (~440 MB) and `/aws/lambda/lorrgs-sqs` (~510 MB): the new Lambdas reuse them. Consider a retention period.
- CloudFront `E3F7N7BKL3F1R3` (`assets.lorrgs.io`).
- Stacks `CDKToolkit`, `discord-notification`, `convert-images`, `aws-sam-cli-managed-default`.
