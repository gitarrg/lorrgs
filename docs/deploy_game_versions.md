# Deploy Mists + Forever (CDK)

`infra/` is a CDK app (Python) for every Game Version except Retail. Retail is not deployed by anything yet.

| Stack | Contains |
| --- | --- |
| `lorrgs-shared` | Lambda layers `lorrgs-shared-requirements` and `lorrgs-shared-core` (shared by all Game Versions) |
| `lorrgs-<version>` | 2 FIFO queues, `-api` and `-sqs` Lambdas (code + SQS triggers), 6h refresh schedule, API Gateway HTTP API, CloudFront distribution, IAM roles |

`scripts/deploy` wraps the CDK CLI (`npx aws-cdk@2`); `scripts/deploy --help` lists the usual commands. If jsii complains about its package cache, set `JSII_RUNTIME_PACKAGE_CACHE_ROOT` to a private directory.

## One-time

1. `scripts/deploy bootstrap aws://746912274922/eu-west-1`
2. Put the credentials in `.env` (repo root): the keys in `SECRETS` (`infra/stacks.py`). The deploy copies them onto the Lambdas; use the Retail values.
3. Mists was created by the old setup script and CDK can't adopt those resources. Delete them first (they hold no data): Lambdas `lorrgs-mists-api` / `lorrgs-mists-sqs`, queues `lorrgs-mists-main.fifo` / `lorrgs-mists-user-reports.fifo`, schedule `lorrgs-mists-load_spec_rankings`.

## Deploy

```bash
scripts/deploy diff    # dry run
scripts/deploy         # deploy all stacks
```

Code or layer changes are picked up by the same command. Assets are hashed by their sources (package folder, `uv.lock`); unchanged ones are not rebuilt or uploaded.
A changed credential in `.env` (e.g. the yearly `WCL_AUTH_TOKEN`) is only picked up by a deploy.

## Cloudflare

CloudFront has no custom domain; Cloudflare stays in front.

- DNS: proxied CNAME `<version>-api` → the stack output `DistributionDomain`.
- Origin Rule per hostname: Host Header = the `DistributionDomain` value.
- Check: `curl https://mists-api.lorrgs.io/api/game_versions`

## Later

- Enable the refresh schedule once there is boss data: `GAME_VERSIONS` in `infra/app.py`.
- Forever `wcl_game_version=99` is a placeholder until #86.
