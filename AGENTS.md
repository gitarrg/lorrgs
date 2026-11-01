# AGENTS.md

Backend for [lorrgs.io](https://lorrgs.io): compares cooldown usage in top Warcraft Logs reports by spec, comp, or a user's own report.

## Related repos

- **Frontend**: `~/wow/lorrgs-frontend`. React + TS + Vite, hosted on Cloudflare Pages. Calls this API via plain GETs (`VITE_BACKEND_URL`: `http://127.0.0.1:5012` dev, `https://api2.lorrgs.io` prod) and loads images from `https://assets2.lorrgs.io`. Check it before changing any `/api/*` route or response shape.
- **TimelineReminders addon**: `~/wow/TimelineReminders`. Does a similar job in-game; the good reference for boss spell IDs, durations, cast timings and phase triggers (`TimelineData/<Expansion>/{Raids,Dungeons}/<Instance>/<Boss>.lua`). Being an addon it has in-game data we lack: spell names and icons must be looked up separately.

## Architecture

Python 3.13, `uv`, FastAPI, pydantic, aiohttp. Three AWS Lambda functions:

- `lorrgs_api/`: FastAPI app wrapped by Mangum; all routes under `/api` (docs at `/api/docs`). Served via Cloudflare at `api2.lorrgs.io`.
- `lorrgs_sqs/`: SQS task worker (`plan_spec_rankings`, `load_spec_rankings`, `load_comp_rankings`, `load_user_report`, `discord`). A scheduled message at minute 1 of every hour queues `plan_spec_rankings`: the Refresh Planner (`lorgs/models/refresh_planner.py`) picks the stalest Spec Rankings of every Game Version with `updates_enabled` that fit the hour's Warcraft Logs points budget, and queues one `load_spec_rankings` task (`limit=50`) each, in the Game Version's FIFO message group (`queue_updates.py --plan` queues a plan by hand, `scripts/plan_spec_rankings.py --queue` runs it locally); payloads with keywords expand into many messages that get re-queued.
- `lorrgs_stats/`: pushes metrics to Grafana.

Shared library `lorgs/`:

- `clients/wcl/`: Warcraft Logs v2 GraphQL client ([API docs](https://www.warcraftlogs.com/v2-api-docs/warcraft/)).
- `clients/discord/`: OAuth login + bot messages.
- `loaders/`: the only path to Warcraft Logs: query building and response parsing for spec rankings, user reports and comp rankings. Models are plain data and never query WCL.
- `models/`: persistence per type: S3 (`SpecRanking`, `CompRanking`), DynamoDB (`UserReport`, `User`), Redis (`Task`), `StaticModel` for hand-written game data (owned by one Game Version's `GameData`).
- `data/`: hand-written game data. `constants.py` is shared; `expansions/<xpac>/{raids,dungeons}/` is the shared boss/dungeon library (one file per boss); each Game Version has its own package (with its own `roles.py`): `retail/` (`classes/` for spec cooldowns, `racials.py`, `externals.py`, `items/`, `seasons/`, and it imports the expansions Retail uses), `forever/` (beta classes and specs, and the Classic raids from `expansions/classic/`; no spells or boss spells yet) and `mists/` (classes with their major cooldowns, and the Mists of Pandaria raids; no boss spells yet). Each version package has a `version.py` that builds its `GameData` (`lorgs/models/game_data.py`, from explicit lists of roles, classes and stand-alone spells, and its current season) and a `GameVersion` that owns it (`lorgs/models/game_version.py`: name, title, WCL id, frontend settings): the `GameData` indexes specs, spells (with variations) and bosses, holds the ranked difficulties and fills in `role.specs`, `class.specs` and `boss.zone`. `import lorgs.data` loads every Game Version: `GAME_VERSIONS` (by name), `RETAIL`, `MISTS`, `FOREVER`, `get_game_version_by_wcl_id()`. There is no active Game Version and no env var picking one: routes, SQS handlers and loaders get a `GameVersion` (or its `.data`) explicitly. Code outside `data/` never imports a version package.

## Game data

Adding raids, bosses, dungeons, seasons, or spells: follow `.cursor/skills/wow-encounter-data/SKILL.md`.

- Copy the nearest finished boss/spec in the same raid or expansion for style (colors, comments, `show=False`).
- Spell names: `data/SpellName.csv`; other DB2 tables in `data/*.csv` (gitignored, refresh with `data/download.sh` from wago.tools). Icons: `curl -sL https://nether.wowhead.com/tooltip/spell/<id>` → `<icon>.jpg`.
- A `RaidZone` that ranks a single difficulty sets `difficulty=` (all MoP raids: Heroic, the highest WCL has). The `auto` difficulty token (routes, payloads, `queue_updates.py`) resolves to it per boss via `GameData.resolve_difficulty()`, and `all` only expands to it; the frontend then hides the difficulty dropdown.
- Selectors (spec, boss, difficulty, metric, each a value or `all`) turn into Spec Rankings in one place: `lorgs/models/selectors.py`. API routes, SQS expanders and scripts use it; don't re-derive `all` or a default metric elsewhere. `all` specs means playable ones: roles with `playable=False` (Retail's `ITEM_ROLE`) hold pseudo-specs (`other-trinkets`, `other-racials`, ...) that are spell groups, not something a player is.
- Bosses with non-standard phases subclass `RaidBoss` and override `phase_from_transition()` (e.g. Venomous Abyss: Coiled Altar, Entombed Sentinels, Lost Explorers).
- Minor rotational spells and tank hits get `show=False`. Replacement spell IDs go in `variations=[...]`.
- A `process_casts` test feeds Casts that Actor Type would load: spell ids registered with `add_spell`, `add_buff`, or `add_debuff` and `query=True`, durations from the spell tooltip. Spell ids come from those registrations, not from an old `actor.load` handler.

## Known state

- Each Game Version's `GameData` holds only its current season (`GameData(season=...)`, which also activates it), so older-season bosses, zones, spells, consumables and seasons are not served by the API (404 or missing from lists). Intended since 34cde07. The old season modules stay in `seasons/` as history.
- Game Versions (#110-#113 done, ADR 0003): the code serves every Game Version, and `infra/` has the `lorrgs` stack serving all of them (`api.lorrgs.io`, shared queues, one hourly Refresh Planner schedule (minute 1, enabled while any `SCHEDULES` entry is; the planner covers the Game Versions with `GameVersion.updates_enabled`) and a daily Builds schedule per version with talents). The old per-version stacks are gone from the CDK app but still deployed until deleted. Not yet deployed or cut over (#116): the frontend switch, copying Retail's un-prefixed S3 rankings to `retail/` are the open cutover steps; until then Retail rankings in S3 are unreachable.
- `/api/user_reports/{id}/load` needs the overview loaded first (`load_overview`): the report's Game Version comes from its log (`masterData.gameVersion`), not from the path. Responses carry the raw Warcraft Logs id; map it with `wcl_game_version` from `/api/game_versions`.
- Several files use CRLF line endings (e.g. `raid_zone.py`, `wow_role.py`, `wow_spell.py`, `api_spec_rankings.py`, `api_world_data.py`). Editing them with Python text-mode I/O silently converts them to LF and makes the diff whole-file: preserve CRLF (`git diff --stat` should stay small).
- Tests build `GameData` with the required `difficulties=` argument; use `test/helpers.py` (`game_data_with`, `game_version_with`) for fixtures. `test/loader/` and `test/integration/` are manual scripts, not collected by pytest.
- Talents (Retail only, `GameVersion.has_talents`): a Spec Ranking player stores `talents`, node entry ids with their rank (`{entry id: rank}`), copied from the rankings query on every Refresh, also onto stored players. Talent trees per spec are `lorgs/data/retail/talent_trees.json`, generated by `scripts/generate_talent_trees.py` from the DB2 CSVs (`data/download.sh`) and served at `/api/{game_version}/talent_trees/{spec_slug}`.
- Builds (Retail only, #126): `lorgs/models/spec_builds.py` holds the pure grouping (`find_builds`, distances in talent nodes, constants `START_THRESHOLD`, `CAP_THRESHOLD`, `COVER`, `MIN_SHARE`, `MAX_BUILDS`, `MERGE_DISTANCE`, `ASSIGN_REACH`) and the stored `SpecBuilds` (S3 `{game_version}/spec_builds/{season_slug}/{spec_slug}`). The `load_spec_builds` SQS task (`spec_slug` or `all`) reads the stored Spec Rankings of the spec's default metric, across all bosses and difficulties; a daily schedule in `infra/` queues it (03:30 + the version's hour offset; `builds_enabled` in `SCHEDULES`, on for Retail), and `queue_updates.py --builds --spec <slug>` re-queues by hand. Per-spec overrides are `WowSpec.builds_ignore` and `builds_force_new` (raw entry ids). Served at `/api/{game_version}/builds/{spec_slug}`.
- Refresh Planner (#131, #132): it replaces the per-version 6h ranking schedules. It does not check whether the previous hour's tasks are still queued; `SpecRanking.needs_refresh()` (2h window) skips duplicates. Dirty rankings are queued with `dirty=True`.
- Comp Rankings are an abandoned feature. The model, routes, and SQS handler remain; `CompRanking.load` fetches the ranking page and does not load fight events.

## Commands

- Install: `uv sync`. Use `.venv`; a stale `VIRTUAL_ENV` from another project picks the wrong packages.
- Dev server: `scripts/start_flask` (uvicorn on `:5012`, reads `.env`; see `template.env`).
- One dev server serves every Game Version. Versioned routes live under `/api/{game_version}/` (spec_ranking, comp_ranking, roles, classes, specs, spells, trinkets, zones, bosses, seasons); global ones have no prefix (`game_versions`, `user_reports`, `tasks`, `auth`, `ping`). `GET /api/game_versions` lists all Game Versions with their frontend settings (`collapse_raids`, `has_comp_modes`) and their `wcl_game_version`, which a User Report's `game_version` refers to (its Game Version comes from its log).
- Stored rankings have a required `game_version` and S3 keys `{game_version}/{table}/...` (Retail too). A Spec Ranking key is `{game_version}/spec_ranking/{season_slug}/{spec_slug}/{boss_slug}__{difficulty}__{metric}`, using the current season of its Game Version. SQS payloads carry a required `game_version`, which is also the start of the FIFO message group; `queue_updates.py --game-version <name>` picks it.
- Tests, one run for every Game Version: `PYTHONPATH=. uv run pytest test`
  - Tests that use real game data live in `test/data_retail/`, `test/data_forever/` or `test/data_mists/`; they all run together. Every other test builds what it needs from fixtures (`test/conftest.py`).
  - `test_task.py` is skipped: it needs a Redis on `localhost:6379`.
- Scripts use the shebang `#!/usr/bin/env -S PYTHONPATH=. uv run`; e.g. `scripts/load_report.py <wcl report url>`.
- Deploy: `scripts/deploy` (CDK app in `infra/`: one stack, `lorrgs`, holding the Lambda layers, code, queues, schedules, API Gateway and CloudFront). See `docs/deploy_game_versions.md`. Pushing to `main` only syncs `lorrgs_assets/` to S3 (GitHub Action). There is no PR CI.
- Logs: `aws logs tail /aws/lambda/lorrgs-api --follow --since 10m`.
- Spec Ranking views per metric (#130): every served ranking logs `spec_ranking_view game_version=.. spec=.. boss=.. difficulty=.. metric=.. default_metric=..` (whether the metric is the spec's default; the frontend always sends one). Only cache misses reach the Lambda (`max-age=300` at Cloudflare, CloudFront and the browser), so popular metrics are undercounted; good for "is this metric used at all". Counted by the saved Logs Insights query `lorrgs/spec-ranking-views` (eu-west-1, `SPEC_RANKING_VIEWS_QUERY` in `infra/stacks.py`); the CloudWatch dashboard `lorrgs-spec-ranking-views` graphs views per (resolved) difficulty for each Game Version.
- `WCL_AUTH_TOKEN` in `.env` and the Lambdas expires yearly.

## Agent skills

### Issue tracker

Issues are tracked in GitHub Issues on `gitarrg/lorrgs` via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
