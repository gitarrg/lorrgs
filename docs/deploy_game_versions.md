# Deploy Mists + Forever (CDK)

> The code serves every Game Version from any deployment (ADR 0003: `/api/{game_version}/...`, `game_version` in every SQS payload). The per-version stacks below still exist until the cutover to one shared deployment, so each stack's Lambdas can read and write every Game Version's S3 prefix and its schedule queues refreshes for its own Game Version only.

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

CloudFront accepts `Host: <version>-api.lorrgs.io` because that name is an alternate domain on the distribution. The viewer certificate is the existing `*.lorrgs.io` cert (`API_CERTIFICATE_ARN` in `infra/stacks.py`). Cloudflare only proxies; it does not rewrite the Host header.

**DNS → Records** in the `lorrgs.io` zone. One proxied CNAME per Game Version, aimed at the stack output `DistributionDomain`.

| Type | Name | Target | Proxy |
| --- | --- | --- | --- |
| CNAME | `mists-api` | `d3unhum4eh0gk0.cloudfront.net` | Proxied |
| CNAME | `forever-api` | `d18wjavgpzemrj.cloudfront.net` | Proxied |

`scripts/deploy` attaches the certificate and the alternate domain, and sets the viewer protocol policy to HTTP and HTTPS. Cloudflare connects to CloudFront over HTTP, so redirecting that hop to HTTPS loops. Browsers still use HTTPS up to Cloudflare. No new DNS records.

### Check

```bash
curl -sI -H "Origin: https://multi-version.lorrgs-frontend.pages.dev" https://forever-api.lorrgs.io/api/roles
```

Expect `HTTP/2 200` and `access-control-allow-origin` echoing that origin. A CloudFront HTML 403 means the alternate domain is not on the distribution yet.

## Later

- Enable the refresh schedule once there is boss data: `GAME_VERSIONS` in `infra/app.py`.
- Forever `wcl_game_version=99` is a placeholder until #86.
