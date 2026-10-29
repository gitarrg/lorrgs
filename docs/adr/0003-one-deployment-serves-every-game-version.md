---
status: accepted
---

# One deployment serves every Game Version

Supersedes [ADR 0002](0002-one-deployment-per-game-version.md). One API Lambda and one SQS Lambda now serve every Game Version, instead of one stack of Lambdas, queues, API Gateway and CloudFront per Game Version. Versioned API routes carry the Game Version in their path (`/api/{game_version}/...` on one host). The router resolves it to a `GameVersion` once, and routes and SQS handlers pass it explicitly to the loaders. There is no process-wide active Game Version, no ambient context variable and no `MemoryModel` registry. Each Game Version owns a `GameData` object: its roles, classes, specs, spells, raids, bosses, dungeons and seasons, indexed for lookup. Every process loads every Game Version's Game Data at import.

## Decisions

- **Explicit, not ambient.** A request-scoped `ContextVar` was considered and rejected for the end state: it is the same hidden global as the old `ACTIVE`, just scoped to a request.
- **One owner per object.** Every Game Data object belongs to exactly one `GameData`, so objects can hold direct references to each other, back-references included (`role.specs`, `class.specs`). Roles are copied into each Game Version's package rather than shared. A module in `expansions/` is imported by one Game Version at a time; the first time a second one needs it, it becomes a factory.
- **Stored data holds ids only.** Rankings, reports, fights, players and casts store slugs and spell ids and never look up Game Data themselves. Loaders resolve everything.
- **Stored rankings name their Game Version**, both as a field and as the S3 key prefix (Retail too, under `retail/`).
- **User Reports stay global.** Their routes have no Game Version in the path. A User Report's Game Version comes from its log (Warcraft Logs `masterData.gameVersion`), because report codes are unique across every Warcraft Logs site.
- **Shared queues.** Task payloads carry a required `game_version`, which is also part of the FIFO message group. Each Game Version has its own refresh schedule, offset by one hour from the others so their refreshes don't land in the same hour of the Warcraft Logs rate-limit quota.

## Considered Options

- **Header per hostname** (keep `<version>-api.lorrgs.io`, CloudFront adds a header): no frontend change, but the version is hidden from the URL and there is one distribution per version.
- **Import the app once per Game Version in one process**: almost no code change, but imports inside functions resolve to whichever copy was imported last.
- **Three processes behind the Lambda Web Adapter**: full isolation, but about three times the memory and cold start.

## Consequences

- Tests that use real Game Data run for every Game Version in one pytest run.
- `GameVersion.api_url` and `deploy_prefix` go away. Infra and scripts import the full Game Data.
- Cutover: the old per-version deployments keep serving their hosts until the frontend switches. Retail's rankings are copied to `retail/` at cutover.
