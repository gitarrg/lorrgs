---
name: wow-encounter-data
description: Add World of Warcraft raid zones, bosses, dungeons, and seasons to lorgs data, including spell IDs, icons, names, and durations. Use when adding a new raid, boss, dungeon, or season, filling ICON_PLACEHOLDER, or looking up spell info from Wowhead/Wago.
---

# WoW Encounter Data

Copy an existing file in the same expansion. Match style of nearby bosses, not older raids.

## Add new raids / bosses / dungeons

**Dungeon stub**

- `lorgs/data/expansions/<exp>/dungeons/<slug>.py` → `Dungeon(name="...")`
- Export from `dungeons/__init__.py` (and expansion `__init__.py` if that expansion re-exports dungeons)

**Raid stub**

- `lorgs/data/expansions/<exp>/raids/<slug>/__init__.py` → `RaidZone(id=, name=, icon=, bosses=[])`
- `id` is the Warcraft Logs zone ID (`https://www.warcraftlogs.com/zone/rankings/<id>`)
- Multi-wing tiers may use floats (`46.1`, `51.2`)
- Encounter IDs: `https://wago.tools/db2/DungeonEncounter/csv` (filter `MapID`)
- Export from `raids/__init__.py` and the expansion `__init__.py`

**Boss file**

- One file per boss next to the raid `__init__.py`
- `RaidBoss(id=<DungeonEncounter ID>, name=, nick=, icon=)` then `boss = CONST`
- Wire `bosses=[...]` in raid order (wiki / OrderIndex / WCL)
- Empty `bosses=[]` / no spells is fine until data exists

**Season**

- Copy `seasons/<exp>_sN.py`: `Season(name, slug, ilvl, raids, dungeons)`
- Export from `seasons/__init__.py` and expansion `__init__.py`
- Only change `lorgs/data/season.py` `CURRENT_SEASON` when asked

## Find spell information (icons, names, cast times, infos)

**IDs / names**

- Timeline Lua (e.g. `data/VenomousAbyss/*.lua`): `value = <spell_id>` plus `-- Name` comments
- Local CSV: `data/SpellName.csv` (`ID,Name`). Refresh via `data/download.sh` if missing
- User-pasted Wowhead links in the boss file

**Icons, cast/channel time, tooltip text**

```bash
curl -sL "https://nether.wowhead.com/tooltip/spell/<SPELL_ID>"
```

JSON: `name`, `icon` (use `<icon>.jpg`), `tooltip` (cast/channel/duration + mechanic text)

**Fallback**

- Full page: `https://www.wowhead.com/spell=<id>` — grep `.jpg`
- Journal: `https://warcraft.wiki.gg/wiki/<Boss>`
- If `icon` is numeric (`8125100`), store `8125100.jpg`

**What to put on `add_cast` / `add_buff`**

- `duration`: mechanic length on the timeline (channel, shield, soak window), **not** always the cast time
- Tank hits: `show=False`
- Short comment from the tooltip under the spell
- Prefer mythic `events` list + heroic for anything commented out in mythic

## Tricks

- Copy a finished boss in the same raid for colors, comments, and `show=False` choices
- Lua `events` (colored, `show=true`) is the spell list; ignore `PHASE_*` / empty placeholder `109998`
- `duration` in Lua entries `{time, duration}` is a good default; keep a longer value if it is already a known window (e.g. bubble lifetime 45s vs 5s cast)
- `add_buff` for apply/burn windows (hearts, weaken debuffs); `variations=[...]` for related IDs
- Do not switch `CURRENT_SEASON` just because a new season file exists
- Verify: import the zone and print `[(b.id, b.name, len(b.spells)) for b in zone.bosses]`
