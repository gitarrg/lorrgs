# Actor-specific behaviour lives in Actor Type subclasses, not signal handlers

Fixes that only apply to a particular spec or boss, such as dropping Tree of Life recasts, deriving Stasis durations or rewriting Nek'zali's phases, used to be global `blinker` handlers on `actor.load`. They ran on every Actor, after the cast counters had been computed, in import order. No test exercised them, and one of them raced the phase loading. Now each Actor Type that needs behaviour is a subclass (`class RestorationDruid(WowSpec)`, `class Nekzali(RaidBoss)`) that overrides `process_casts(casts) -> casts` or `process_phases(phases, casts) -> phases`. The actor-load pipeline calls these in a fixed place: after sorting and before counters, and for phases only once both the phases and the boss casts are loaded. Each fix is declared on the narrowest type it applies to; class-level steps run before spec-level ones.

## Considered Options

- **Hooks attached to the `WowSpell`**: awkward for fixes that span several spells (Stasis charge/release), and the fix ends up far from the spec that owns it.
- **A central ordered list of post-processors**: explicit, but every new spec or boss fix would mean editing a file outside its data file.
- **Keep `blinker`, but call it at the right moment**: still global and still unordered; every handler keeps re-checking whether the actor is one it cares about.

## Consequences

- The `actor.load` signal remains for task progress reporting only. Handlers must not mutate Actors or Fights.
- A Game Version's `GameData` indexes its Actor Types by what they are (slug, id), not by class, so `game_data.get_spec()` / `get_boss()` find subclass instances. (This used to be the `MemoryModel` registry, which ADR 0003 removed.)
- Only Actor Types that need behaviour are subclasses; plain instances remain valid for everything else.
