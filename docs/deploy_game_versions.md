# Deploy (CDK)

> The code serves every Game Version from any deployment (ADR 0003: `/api/{game_version}/...`, `game_version` in every SQS payload). `lorrgs-all` is the one stack that serves all of them. The old per-version stacks stay up next to it until the frontend cuts over; each of those serves its own host.

`infra/` is a CDK app (Python). Retail has no old stack; it is only in `lorrgs-all`.

| Stack | Contains |
| --- | --- |
| `lorrgs-shared` | Lambda layers `lorrgs-shared-requirements` and `lorrgs-shared-core` (shared by all stacks) |
| `lorrgs-all` | The end state, host `api.lorrgs.io`: 2 FIFO queues (`lorrgs-all-main.fifo`, `lorrgs-all-user-reports.fifo`), `lorrgs-all-api` and `lorrgs-all-sqs` Lambdas, one API Gateway HTTP API, one CloudFront distribution, one refresh schedule per Game Version, IAM roles |
| `lorrgs-<version>` | Old, until cutover (Mists, Forever): the same pieces for one Game Version, host `<version>-api.lorrgs.io`. Not touched by `lorrgs-all` |

`lorrgs-all` shares nothing with the old stacks except the layers; its resources are named `lorrgs-all-*`, so `scripts/deploy diff lorrgs-all -e` shows only new resources.

### Refresh schedules

`lorrgs-all` has one EventBridge schedule per Game Version (`lorrgs-all-load_spec_rankings_<version>`), every 6h, offset by one hour to spread the Warcraft Logs quota (Europe/London):

| Game Version | Hours |
| --- | --- |
| Retail | 0, 6, 12, 18 |
| Mists | 1, 7, 13, 19 |
| Forever | 2, 8, 14, 20 |

Each queues `load_spec_rankings` (with its `game_version`) on the shared main queue, message group `<version>-load_spec_rankings`. They are all disabled; enable one by setting `enabled=True` in `SCHEDULES` (`infra/app.py`) once it has boss data, and deploy. Do not enable Retail's before the cutover: the old Retail deployment still runs its own refresh and its S3 rankings are not yet copied to `retail/`.

`scripts/deploy` wraps the CDK CLI (`npx aws-cdk@2`); `scripts/deploy --help` lists the usual commands. If jsii complains about its package cache, set `JSII_RUNTIME_PACKAGE_CACHE_ROOT` to a private directory.

## One-time

1. `scripts/deploy bootstrap aws://746912274922/eu-west-1`
2. Put the credentials in `.env` (repo root): the keys in `SECRETS` (`infra/stacks.py`). The deploy copies them onto the Lambdas; use the Retail values.
3. (Old Mists stack only) Mists was created by the old setup script and CDK can't adopt those resources. Delete them first (they hold no data): Lambdas `lorrgs-mists-api` / `lorrgs-mists-sqs`, queues `lorrgs-mists-main.fifo` / `lorrgs-mists-user-reports.fifo`, schedule `lorrgs-mists-load_spec_rankings`.

## Deploy

```bash
scripts/deploy diff                  # dry run, all stacks
scripts/deploy diff lorrgs-all -e   # only the new stack
scripts/deploy deploy lorrgs-all    # deploy the new stack (and lorrgs-shared)
scripts/deploy                       # deploy all stacks
```

Code or layer changes are picked up by the same command. Assets are hashed by their sources (package folder, `uv.lock`); unchanged ones are not rebuilt or uploaded.
A changed credential in `.env` (e.g. the yearly `WCL_AUTH_TOKEN`) is only picked up by a deploy.

## Cloudflare

CloudFront accepts `Host: api.lorrgs.io` (and, on the old stacks, `<version>-api.lorrgs.io`) because that name is an alternate domain on the distribution. The viewer certificate is the existing `*.lorrgs.io` cert (`API_CERTIFICATE_ARN`, from `.env`; required to synth). Cloudflare only proxies; it does not rewrite the Host header.

**DNS → Records** in the `lorrgs.io` zone. One proxied CNAME per host, aimed at the stack output `DistributionDomain`.

| Type | Name | Target | Proxy |
| --- | --- | --- | --- |
| CNAME | `api` | `DistributionDomain` of `lorrgs-all` | Proxied |
| CNAME | `mists-api` | `d3unhum4eh0gk0.cloudfront.net` (old) | Proxied |
| CNAME | `forever-api` | `d18wjavgpzemrj.cloudfront.net` (old) | Proxied |

`scripts/deploy` attaches the certificate and the alternate domain, and sets the viewer protocol policy to HTTP and HTTPS. Cloudflare connects to CloudFront over HTTP, so redirecting that hop to HTTPS loops. Browsers still use HTTPS up to Cloudflare. Only the `api` record is new.

### Check

```bash
curl -sI -H "Origin: https://multi-version.lorrgs-frontend.pages.dev" https://api.lorrgs.io/api/mists/roles
```

Expect `HTTP/2 200` and `access-control-allow-origin` echoing that origin (the app sets the CORS headers). A CloudFront HTML 403 means the alternate domain is not on the distribution yet.

## Later

- Cutover (#116): switch the frontend to `api.lorrgs.io`, copy Retail's un-prefixed S3 rankings to `retail/`, enable the schedules, delete the old stacks.
- Forever `wcl_game_version=99` is a placeholder until #86.
