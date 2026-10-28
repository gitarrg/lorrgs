# Deploy Mists + Forever

No code changes needed. IAM and CORS (incl. `*.lorrgs-frontend.pages.dev`) are already fine.

## 1. AWS resources

- Needs `uv` on the PATH (`PATH=$PATH:~/.local/bin`).
- Dry run, then apply:
  ```bash
  for v in mists forever; do scripts/setup_game_version.py $v; done
  for v in mists forever; do scripts/setup_game_version.py $v --apply; done
  ```
- Note the printed Function URLs (`https://xxxx.lambda-url.eu-west-1.on.aws/`).
- Creates per version: 2 FIFO queues, 2 Lambdas, SQS triggers, Function URL, DISABLED 6h schedule.

## 2. Deploy code

- Push to `main` (GitHub Action), or manually:
  ```bash
  AWS_CONFIG_FILE=.github/workflows/aws_config PYTHONPATH=. uv run python scripts/deploy.py
  ```

## 3. API URL env vars

- The setup script already sets `LORRGS_API_URL_RETAIL`, `LORRGS_API_URL_MISTS`, and `LORRGS_API_URL_FOREVER` on the new Lambdas (`lorrgs-mists-api`, `lorrgs-forever-api`, and the `sqs` ones). Retail (`lorrgs-api`) still needs them set by hand:
  ```
  LORRGS_API_URL_RETAIL=https://api2.lorrgs.io
  LORRGS_API_URL_MISTS=https://mists-api.lorrgs.io
  LORRGS_API_URL_FOREVER=https://forever-api.lorrgs.io
  ```
- Credentials are not copied. Set `WCL_*`, `DISCORD_*`, `REDIS_URL`, `SECRET_KEY`, and `MONGO_URI` on the new Lambdas (same values as Retail).
- Without the API urls the version doesn't show in the frontend menu.

## 4. Cloudflare

- DNS: proxied CNAMEs, host only (no `https://`, no trailing `/`):
  - `mists-api` → mists Function URL host
  - `forever-api` → forever Function URL host
- Origin Rule per hostname (Rules → Origin Rules):
  - Match `http.host eq "mists-api.lorrgs.io"` (same for forever)
  - Set Host Header to the Function URL host (Lambda URLs reject other Hosts)
- Check: `curl https://mists-api.lorrgs.io/api/game_versions`

## 5. Frontend preview

```bash
cd ~/wow/lorrgs-frontend
git push -u origin multi_version
```

- Pages builds a preview at `https://multi-version.lorrgs-frontend.pages.dev` (check Pages → Deployments).
- No Pages env vars needed (uses `api2.lorrgs.io`). Production stays on `main`.

## 6. Later

- Enable the schedules in EventBridge Scheduler once there is boss data: `lorrgs-mists-load_spec_rankings`, `lorrgs-forever-load_spec_rankings`.
- Forever `wcl_game_version=99` is a placeholder until #86.
- `WCL_AUTH_TOKEN` expires yearly; rotate it on all Lambdas.
