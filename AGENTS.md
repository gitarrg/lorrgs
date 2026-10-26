# AGENTS.md

Backend for [lorrgs.io](https://lorrgs.io): compares cooldown usage in top Warcraft Logs reports by spec, comp, or a user's own report.

## Related repos

- **Frontend**: `~/wow/lorrgs-frontend`. React + TS + Vite, hosted on Cloudflare Pages. Calls this API via plain GETs (`VITE_BACKEND_URL`: `http://127.0.0.1:5012` dev, `https://api2.lorrgs.io` prod) and loads images from `https://assets2.lorrgs.io`. Check it before changing any `/api/*` route or response shape.
- **TimelineReminders addon**: `~/wow/TimelineReminders`. Does a similar job in-game; the good reference for boss spell IDs, durations, cast timings and phase triggers (`TimelineData/<Expansion>/{Raids,Dungeons}/<Instance>/<Boss>.lua`). Being an addon it has in-game data we lack: spell names and icons must be looked up separately.

## Architecture

Python 3.13, `uv`, FastAPI, pydantic, aiohttp. Three AWS Lambda functions:

- `lorrgs_api/`: FastAPI app wrapped by Mangum; all routes under `/api` (docs at `/api/docs`). Served via Cloudflare at `api2.lorrgs.io`.
- `lorrgs_sqs/`: SQS task worker (`load_spec_rankings`, `load_comp_rankings`, `load_user_report`, `discord`). A scheduled message every 6h triggers ranking refreshes; payloads with keywords expand into many messages that get re-queued.
- `lorrgs_stats/`: pushes metrics to Grafana.

Shared library `lorgs/`:

- `clients/wcl/`: Warcraft Logs v2 GraphQL client ([API docs](https://www.warcraftlogs.com/v2-api-docs/warcraft/)).
- `clients/discord/`: OAuth login + bot messages.
- `loaders/`: WCL query building and response parsing (loader extraction is an ongoing refactor; some models still query WCL themselves via `wclclient_mixin`).
- `models/`: persistence per type: S3 (`SpecRanking`, `CompRanking`), DynamoDB (`UserReport`, `User`), Redis (`Task`), in-memory `MemoryModel` for static game data.
- `data/`: hand-written game data. `roles.py` and `constants.py` are shared; `expansions/<xpac>/{raids,dungeons}/` is the shared boss/dungeon library (one file per boss); each Game Version has its own package that `LORRGS_GAME_VERSION` picks: `retail/` (`classes/` for spec cooldowns, `racials.py`, `externals.py`, `items/`, `seasons/`, `season.py` with `CURRENT_SEASON`, and it imports the expansions Retail uses), `forever/` and `classic_mop/` (empty skeletons). Code outside `data/` reads game data via `from lorgs.data import ...` or the registries, never from a version package.

## Game data

Adding raids, bosses, dungeons, seasons, or spells: follow `.cursor/skills/wow-encounter-data/SKILL.md`.

- Copy the nearest finished boss/spec in the same raid or expansion for style (colors, comments, `show=False`).
- Spell names: `data/SpellName.csv`; other DB2 tables in `data/*.csv` (gitignored, refresh with `data/download.sh` from wago.tools). Icons: `curl -sL https://nether.wowhead.com/tooltip/spell/<id>` → `<icon>.jpg`.
- Bosses with non-standard phases subclass `RaidBoss` and override `phase_from_transition()` (e.g. Venomous Abyss: Coiled Altar, Entombed Sentinels, Lost Explorers).
- Minor rotational spells and tank hits get `show=False`. Replacement spell IDs go in `variations=[...]`.
- A `process_casts` test feeds Casts that Actor Type would load: spell ids registered with `add_spell`, `add_buff`, or `add_debuff` and `query=True`, durations from the spell tooltip. Spell ids come from those registrations, not from an old `actor.load` handler.

## Commands

- Install: `uv sync`. Use `.venv`; a stale `VIRTUAL_ENV` from another project breaks `MemoryModel`.
- Dev server: `scripts/start_flask` (uvicorn on `:5012`, reads `.env`; see `template.env`).
- Tests, one run per Game Version:
  - Retail: `PYTHONPATH=. uv run pytest test --ignore=test/data_forever --ignore=test/data_classic_mop`
  - Forever: `LORRGS_GAME_VERSION=forever PYTHONPATH=. uv run pytest test/data_forever`
  - Classic MoP: `LORRGS_GAME_VERSION=classic_mop PYTHONPATH=. uv run pytest test/data_classic_mop`
  - Tests that use real game data live in `test/data_retail/`, `test/data_forever/` or `test/data_classic_mop/`; a `conftest.py` aborts the run if `LORRGS_GAME_VERSION` doesn't match the directory. Every other test builds what it needs from fixtures (`test/conftest.py`).
  - `test_task.py` needs a Redis on `localhost:6379`.
- Scripts use the shebang `#!/usr/bin/env -S PYTHONPATH=. uv run`; e.g. `scripts/load_report.py <wcl report url>`.
- Deploy: push to `main`. The GitHub Action syncs `lorrgs_assets/` to S3 and runs `scripts/deploy.py` (Lambda layers + code). There is no PR CI.
- Logs: `aws logs tail /aws/lambda/lorrgs-api --follow --since 10m`.
- `WCL_AUTH_TOKEN` in `.env` and the Lambdas expires yearly.

## Agent skills

### Issue tracker

Issues are tracked in GitHub Issues on `gitarrg/lorrgs` via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
