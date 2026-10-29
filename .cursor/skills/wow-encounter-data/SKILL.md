---
name: wow-encounter-data
description: Add World of Warcraft raid zones, bosses, dungeons, and seasons to lorgs data, including spell IDs, icons, names, and durations. Use when adding a new raid, boss, dungeon, or season, filling ICON_PLACEHOLDER, or looking up spell info from Wowhead/Wago.
---

# WoW Encounter Data

Copy an existing file in the same expansion. Match style of nearby bosses, not older raids.

**New patch:** run `data/download.sh` first. New-patch spell IDs are missing from `data/SpellName.csv` (and the other `data/*.csv` DB2 tables) until that refresh.

## Add new raids / bosses / dungeons

**Dungeon stub**

- `lorgs/data/expansions/<exp>/dungeons/<slug>.py` → `Dungeon(name="...")`
- Export from `dungeons/__init__.py` (and expansion `__init__.py` if that expansion re-exports dungeons)

**Raid stub**

- `lorgs/data/expansions/<exp>/raids/<slug>/__init__.py` → `RaidZone(id=, name=, icon=, bosses=[])`
- `id` is the Warcraft Logs zone ID (`https://www.warcraftlogs.com/zone/rankings/<id>`)
- Zone and encounter IDs: `scripts/list_wcl_zones.py` (optional name filter).
- Multi-wing tiers may use floats (`46.1`, `51.2`)
- Encounter IDs also in `https://wago.tools/db2/DungeonEncounter/csv` (filter `MapID`)
- Export from `raids/__init__.py` and the expansion `__init__.py`
- A new expansion package must also be imported by `lorgs/data/retail/__init__.py` (each Game Version's package imports the expansions it uses)

**Boss file**

- One file per boss next to the raid `__init__.py`
- `RaidBoss(id=<DungeonEncounter ID>, name=, nick=, icon=)` then `boss = CONST`
- Wire `bosses=[...]` in raid order (wiki / OrderIndex / WCL)
- Empty `bosses=[]` / no spells is fine until data exists

**Season**

- Copy `lorgs/data/retail/seasons/<exp>_sN.py`: `Season(name, slug, ilvl, raids, dungeons)`
- Export from `lorgs/data/retail/seasons/__init__.py`
- Only change the current season (`season=` in `lorgs/data/retail/version.py`) when asked

## Find spell information (icons, names, cast times, infos)

**IDs / names**

- Timeline Lua (e.g. `data/VenomousAbyss/*.lua`): `value = <spell_id>` plus `-- Name` comments
- Local CSV: `data/SpellName.csv` (`ID,Name`). If an ID is missing, the tables are stale — run `data/download.sh`
- User-pasted Wowhead links in the boss file

**Icons, cast/channel time, tooltip text**

```bash
curl -sL "https://nether.wowhead.com/tooltip/spell/<SPELL_ID>"
```

JSON: `name`, `icon` (use `<icon>.jpg`), `tooltip` (cast/channel/duration + mechanic text)

**Icons must exist**

- Store only a filename that returns 200 at `https://wow.zamimg.com/images/wow/icons/large/<icon>.jpg` (`curl -sI`). A numeric TimelineReminders icon such as `537022` 404s there.
- For Bosses and zones: use the Wowhead achievement icon (Kith'ix: `8214194.jpg`).

**Fallback**

- Full page: `https://www.wowhead.com/spell=<id>` — grep `.jpg`, then confirm the zamimg URL
- Journal: `https://warcraft.wiki.gg/wiki/<Boss>`

**Cast, buff, or debuff**

Many mechanics are not cast events. Check the event type in a log, then call the matching helper:

- `boss.add_cast` for casts
- `boss.add_debuff` for auras on players
- `boss.add_buff` for auras on the boss

**What to put on the spell**

- `duration`: mechanic length on the timeline (channel, shield, soak window), **not** always the cast time
- Tank hits: `show=False`
- Short comment from the tooltip under the spell
- Prefer mythic `events` list + heroic for anything commented out in mythic

## Tricks

- Copy a finished boss in the same raid for colors, comments, and `show=False` choices
- Lua `events` (colored, `show=true`) is the spell list; ignore `PHASE_*` / empty placeholder `109998`
- `duration` in Lua entries `{time, duration}` is a good default; keep a longer value if it is already a known window (e.g. bubble lifetime 45s vs 5s cast)
- `variations=[...]` for related IDs
- Do not switch the current season just because a new season file exists
- Verify: import the zone and print `[(b.id, b.name, len(b.spells)) for b in zone.bosses]`
