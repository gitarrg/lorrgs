# Deploy (CDK)

> The code serves every Game Version from one deployment (ADR 0003: `/api/{game_version}/...`, `game_version` in every SQS payload).

`infra/` is a CDK app (Python) with two stacks:

| Stack | Contains |
| --- | --- |
| `lorrgs-layers` | Lambda layers `lorrgs-layers-requirements` and `lorrgs-layers-core` |
| `lorrgs` | Host `api.lorrgs.io`: 2 FIFO queues (`lorrgs-main.fifo`, `lorrgs-user-reports.fifo`), `lorrgs-api` and `lorrgs-sqs` Lambdas, one API Gateway HTTP API (`lorrgs-api`), one CloudFront distribution, one refresh schedule per Game Version, IAM roles |

The old per-version stacks (`lorrgs-shared`, `lorrgs-mists`, `lorrgs-forever`) are no longer in the app. CDK does not delete stacks it no longer knows: they keep running until removed (`scripts/deploy destroy` does not see them; use `aws cloudformation delete-stack --stack-name <name>`, see #116).

### Refresh schedules

`lorrgs` has one EventBridge schedule per Game Version (`lorrgs-load_spec_rankings-<version>`), every 6h, offset by one hour to spread the Warcraft Logs quota (Europe/London):

| Game Version | Hours |
| --- | --- |
| Retail | 0, 6, 12, 18 |
| Mists | 1, 7, 13, 19 |
| Forever | 2, 8, 14, 20 |

Each queues `load_spec_rankings` (with its `game_version`) on the main queue, message group `<version>-load_spec_rankings`. They are all disabled; enable one by setting `enabled=True` in `SCHEDULES` (`infra/app.py`) once it has boss data, and deploy. Do not enable Retail's before the cutover: the old Retail deployment still runs its own refresh and its S3 rankings are not yet copied to `retail/`.

`scripts/deploy` wraps the CDK CLI (`npx aws-cdk@2`); `scripts/deploy --help` lists the usual commands. If jsii complains about its package cache, set `JSII_RUNTIME_PACKAGE_CACHE_ROOT` to a private directory.

## One-time

1. `scripts/deploy bootstrap aws://746912274922/eu-west-1`
2. Put the credentials in `.env` (repo root): the keys in `SECRETS` (`infra/stacks.py`). The deploy copies them onto the Lambdas; use the Retail values.

## Deploy

```bash
scripts/deploy diff      # dry run
scripts/deploy           # deploy both stacks
```

Code or layer changes are picked up by the same command. Assets are hashed by their sources (package folder, `uv.lock`); unchanged ones are not rebuilt or uploaded.
A changed credential in `.env` (e.g. the yearly `WCL_AUTH_TOKEN`) is only picked up by a deploy.

## Cloudflare

CloudFront accepts `Host: api.lorrgs.io` because that name is an alternate domain on the distribution. The viewer certificate is the existing `*.lorrgs.io` cert (`API_CERTIFICATE_ARN`, from `.env`; required to synth). Cloudflare only proxies; it does not rewrite the Host header.

**DNS → Records** in the `lorrgs.io` zone. One proxied CNAME, `api`, aimed at the stack output `DistributionDomain`.

| Type | Name | Target | Proxy |
| --- | --- | --- | --- |
| CNAME | `api` | `DistributionDomain` of `lorrgs` | Proxied |

`scripts/deploy` attaches the certificate and the alternate domain, and sets the viewer protocol policy to HTTP and HTTPS. Cloudflare connects to CloudFront over HTTP, so redirecting that hop to HTTPS loops. Browsers still use HTTPS up to Cloudflare.

### Check

```bash
curl -sI -H "Origin: https://multi-version.lorrgs-frontend.pages.dev" https://api.lorrgs.io/api/mists/roles
```

Expect `HTTP/2 200` and `access-control-allow-origin` echoing that origin (the app sets the CORS headers). A CloudFront HTML 403 means the alternate domain is not on the distribution yet.

## Later

- Cutover (#116): switch the frontend to `api.lorrgs.io`, copy Retail's un-prefixed S3 rankings to `retail/`, enable the schedules, delete the old stacks (`lorrgs-shared`, `lorrgs-mists`, `lorrgs-forever`) and the `mists-api` / `forever-api` DNS records.
- Forever `wcl_game_version=99` is a placeholder until #86.
