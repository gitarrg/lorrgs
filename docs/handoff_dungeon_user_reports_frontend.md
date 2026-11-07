# Handoff: show Dungeon runs in User Reports (frontend)

Repo: `~/wow/lorrgs-frontend` (React + TS + Vite). Backend: `~/wow/lorrgs` (done, see below).

## Goal

WoW Forever dungeon runs (and maybe Retail dungeons later) should show up in User Reports. They are never ranked.

## Why they don't show today

The backend already loads a dungeon run as a Fight (difficulty `10`, `fight.dungeon = "<slug>"`, empty `boss: {}`).
The frontend only knows bosses:

- `src/components/ReportNavbar/FightSelectList.tsx` groups pulls by `fight.boss?.boss_slug`. A dungeon run has none, so it falls in an `undefined` group; `BossGroup` calls `get_boss(state, undefined)`, gets `null` and renders nothing. So the run can't be selected.
- `src/types/fight.ts` has no `dungeon` field.
- Nothing in `src` mentions dungeons.

## Backend (done, uncommitted)

- `GET /api/{game_version}/dungeons` -> `{"dungeons": [{id, name, name_slug, icon}]}`. Only dungeons with a Warcraft Logs `id` (loadable ones). Retail returns `[]` until its dungeons get ids.
- `GET /api/{game_version}/dungeons/{dungeon_slug}` -> one dungeon, 404 if unknown.
- `icon` is the same fallback for every dungeon: `inv_misc_map_01.jpg` (`lorgs/models/dungeon.py: FALLBACK_ICON`). `scripts/load_images.py` now uploads dungeon icons, so run it once so the file exists in `assets2.lorrgs.io/images/spells/`.
- Routes and tests: `lorrgs_api/routes/api_world_data.py`, `test/data_forever/test_dungeon_routes.py`.

## To do in the frontend

1. **Types:** add `dungeon?: string` to `Fight` in `src/types/fight.ts`. Add a `Dungeon` type (`id`, `name`, `name_slug`, `icon`, `icon_path`).
2. **Store:** add `src/store/dungeons.ts`, modelled on `src/store/bosses.ts`. Load `/api/{game_version}/dungeons` with the other global data (see `GlobalDataLoader.tsx`; check how it passes the game version). Set `icon_path = `${ASSETS}/images/spells/${icon}`` (same folder as spell icons; `ASSETS` is in `src/constants.ts`). Add a `get_dungeon(state, slug)` selector.
3. **`FightSelectList.tsx`:** group by `fight.boss?.boss_slug ?? fight.dungeon`. Render a `DungeonGroup` next to `BossGroup`, with the dungeon icon (`Icon` takes Spec/Class/Role/Boss, so widen its type or use `WebpImg`/`img` directly) and the dungeon name. Skip the group if the dungeon is unknown, as `BossGroup` does.
4. **`FightWidget`** (same folder): check what it shows. It may use the boss name, or `kill` / `percent`. A dungeon run's `kill` and `percent` may mean something different; the Fight summary has `duration` and `start_time`.
5. **Timeline:** `src/components/Timeline/FightRow.ts:59` only adds a boss row `if (fight_data.boss)`, so a dungeon run just shows its players. Check it renders. Also check `PlayerNamesFight.tsx` (`create_boss` already returns early) and `get_occuring_bosses` in `src/store/fights.ts` / `UserReport.tsx` (must not choke on a fight without a boss).
6. **Report loading:** `src/routes/UserReport/UserReport.tsx` loads boss spells per occurring boss. Dungeon runs have no boss spells; players' spells still load as usual.
7. **Manual check:** open a Forever dungeon report (`/api/user_reports/{id}/load_overview`, then the fights). Needs the backend running (`scripts/start_flask` in the backend repo, `VITE_BACKEND_URL=http://127.0.0.1:5012`).
8. Later: per-dungeon icons (add `icon=` per dungeon in `lorgs/data/forever/dungeons.py`; `load_images.py` already uploads them).

## Notes / traps

- User Report responses carry the raw Warcraft Logs game version id; map with `wcl_game_version` from `/api/game_versions`.
- The test suite on `main` has pre-existing failures unrelated to this: commit `33253bab` ("fix mists import") left `MISTS` out of `lorgs/data/__init__.py`, which breaks collection of several test files. Run `pytest test/data_forever test/data_retail test/test_models/test_warcraftlogs_report.py` to check this work.
- Related notes: `docs/forever_todo.md` (item 4).

## Suggested skills

- `mattpocock-skills:tdd` for the store / grouping logic.
- `run` to start the app and check the change in the browser.
- `claude-in-chrome` to look at the result.
