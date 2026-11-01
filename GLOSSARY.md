# Lorrgs

Compares how top players and raid groups use their cooldowns, using fights recorded on Warcraft Logs.

## Language

**Game Version**:
A separately released edition of World of Warcraft with its own classes, spells, raids and Warcraft Logs rankings, e.g. Retail, WoW Forever or WoW Classic: Mists of Pandaria. Each Game Version is compared only against itself.
_Avoid_: game, flavor, version (alone)

**Game Data**:
The hand-written description of one Game Version's roles, classes, specs, spells, raids, bosses, dungeons and seasons that Lorrgs compares Fights against. Each Game Version has its own Game Data, even where two of them describe the same thing. Every process holds the Game Data of every Game Version, and a lookup only ever sees the one it was made on (`GameVersion.data`).
_Avoid_: static data, world data, registry

**Patch**:
A numbered content update within a Game Version (e.g. 12.0, 12.0.5).
_Avoid_: version

**Fight**:
One pull of a boss inside a Warcraft Logs report, from pull to kill or wipe.
_Avoid_: encounter (that is the boss), pull

**Actor**:
A participant in a Fight whose Casts we track, either a player or the boss.
_Avoid_: unit, source

**Actor Type**:
What kind of Actor something is: a class, a spec or a boss. A spec belongs to a class, and an Actor Type inherits everything its parent type defines.
_Avoid_: actor class, role

**Cast**:
One entry on an Actor's timeline: a spell cast, an aura gained, or a synthetic event derived from them (e.g. dropping Void Metamorphosis).
_Avoid_: event (the raw Warcraft Logs record a Cast is built from)

**Composition**:
How many of each spec and role a raid brought to a Fight.
_Avoid_: comp (in prose), roster, setup

**Raid Cooldown**:
A spell whose effect covers the whole raid (e.g. a raid-wide damage reduction), as opposed to a personal or single-target cooldown.
_Avoid_: raid CD (in prose)

**Spec Ranking**:
The top-ranked Fights on one boss for one spec, showing that spec's Casts.

**Comp Ranking**:
The top-ranked Fights on one boss, showing each raid's Composition and Raid Cooldowns, filterable by Composition.
_Avoid_: comp search

**Talents**:
The exact set of talent choices (with ranks) one player had in one Fight.
_Avoid_: loadout, talent build

**Build**:
A group of Talents of one spec that differ by only a few choices, treated as "the same way to play the spec". Builds are worked out from many Fights, not from one.
_Avoid_: talent build, loadout, spec (alone)

**Refresh**:
Re-fetching a ranking's top Fights from Warcraft Logs and loading the new ones. A ranking is only refreshed when it is stale or Dirty.

**Refresh Planner**:
The hourly job that picks the Spec Rankings to refresh: the ones least recently refreshed, as many as fit the Refresh Budget, across every Game Version.
_Avoid_: scheduler, refresh schedule

**Refresh Budget**:
The Warcraft Logs points the Refresh Planner may spend in one hour: the hourly limit minus a reserve kept for User Reports and manual refreshes.
_Avoid_: quota, rate limit (that is Warcraft Logs' own limit)

**Dirty**:
A ranking flagged for a full reload, because the data it was loaded with changed (e.g. a spell was added). A Dirty ranking is refreshed at the next opportunity, however recently it was last refreshed.

**Phase**:
A named stretch of a Fight, starting at a timestamp. Intermissions are phases with fractional ids (e.g. 1.5).
_Avoid_: stage
