---
status: superseded by ADR-0003
---

# One deployment per Game Version

Lorrgs serves more than one Game Version (Retail, WoW Forever). Each Game Version runs as its own deployment of the same codebase: `LORRGS_GAME_VERSION` picks the data package (`lorgs/data/retail/`, `lorgs/data/forever/`) at import time, and each deployment has its own Lambdas, SQS queue, schedule, S3 key prefix, API host (`api2.lorrgs.io`, `forever-api.lorrgs.io`) and frontend build (`lorrgs.io`, `forever.lorrgs.io`). Retail keeps today's unprefixed S3 keys, so nothing is migrated. Users, roles, image assets, the DynamoDB tables, Redis and the Warcraft Logs API client are shared between Game Versions. The WCL API terms forbid using multiple credentials or circumventing rate limits, so both deployments spend one rate-limit budget. Report codes are unique across all WCL sites, and `www.warcraftlogs.com` serves every site's reports and rankings, so both use one API endpoint. Each User Report records the Game Version of its log (WCL `masterData.gameVersion`), so a log pasted on the wrong site can be sent to the right one. Redis needs no namespace, because Task ids are SQS message ids. Login is shared too: both APIs sign the login token with the same secret, and the frontend keeps it in a cookie on `lorrgs.io`, which every subdomain can read.

## Considered Options

- **One process serving every Game Version**: one deployment, but `MemoryModel` is a process-wide registry, so every lookup (`WowSpec.get()`, `RaidBoss.get()`, ...) would need a Game Version scope, as would every route, task payload and storage key. Only worth it with many Game Versions.
- **Fork the repo per Game Version**: fastest to start, but every fix has to be made twice.

## Consequences

- Code outside `lorgs/data/` must not import a specific Game Version's data; it goes through the registries or the active Game Version's config.
- A single process never holds two Game Versions' data, so tests that use real game data run once per Game Version.
- Infrastructure exists once per Game Version; the CDK app in `infra/` deploys the same layers and code to each Game Version's stack.
