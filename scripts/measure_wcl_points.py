#!/usr/bin/env -S PYTHONPATH=. uv run
"""Measure how many Warcraft Logs points the queries of a Spec Ranking Refresh cost.

Reads `rateLimitData` before and after each query. Other users of the same API key
(the SQS worker) spend points meanwhile, which only ever adds to a reading: the
smallest of several readings is the closest to the real cost.
"""

# IMPORT STANDARD LIBRARIES
import argparse
import asyncio
import statistics
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.clients import wcl
from lorgs.clients.wcl import WarcraftlogsClient
from lorgs.data import GAME_VERSIONS
from lorgs.loaders.boss_loader import BossLoader
from lorgs.loaders.spec_ranking import SpecRankingLoader
from lorgs.models import selectors
from lorgs.models.raid_zone import AUTO_DIFFICULTY
from lorgs.models.warcraftlogs_ranking import SpecRanking


SETTLE = 1.0
"""Seconds to wait before reading the points spent, in case Warcraft Logs books them late."""


async def points_spent(client: WarcraftlogsClient) -> float:
    info = await client.get_rate_info()
    return info["pointsSpentThisHour"]


async def measure(client: WarcraftlogsClient, run: typing.Callable[[], typing.Awaitable[typing.Any]]) -> float:
    before = await points_spent(client)
    await run()
    await asyncio.sleep(SETTLE)
    return await points_spent(client) - before


def report(label: str, costs: list[float], note: str = "") -> None:
    print(f"{label:<28} min {min(costs):>7.2f} | median {statistics.median(costs):>7.2f} | n={len(costs)} {note}")


async def fight_events(client: WarcraftlogsClient, code: str, fight_id: int) -> tuple[int, int]:
    """All events of one fight, unfiltered. Returns (pages, events)."""
    pages, events, start = 0, 0, ""
    while True:
        result = await client.query(
            f'reportData {{ report(code: "{code}") {{ events(fightIDs: [{fight_id}], limit: 10000{start}) '
            "{ data nextPageTimestamp } } }",
        )
        page = result["reportData"]["report"]["events"]
        pages += 1
        events += len(page["data"])
        if not page.get("nextPageTimestamp"):
            return pages, events
        start = f", startTime: {page['nextPageTimestamp']}"


async def main(game_version_name: str, spec_slug: str, boss_slug: str, repeats: int) -> None:  # ruff: ignore[too-many-locals]
    game_version = GAME_VERSIONS[game_version_name]
    game_data = game_version.data
    spec = game_data.get_spec(spec_slug)
    if not spec:
        raise SystemExit(f"unknown spec: {spec_slug}")
    boss_slug = boss_slug or game_data.bosses[0].full_name_slug
    ranking = SpecRanking(
        game_version=game_version.name,
        spec_slug=spec_slug,
        boss_slug=boss_slug,
        difficulty=game_data.resolve_difficulty(boss_slug, AUTO_DIFFICULTY),
        metric=selectors.default_metric(spec),
    )
    loader = SpecRankingLoader(ranking, game_version)
    client = WarcraftlogsClient.get_instance()
    print(f"{game_version.name} | {spec_slug} | {boss_slug} | {ranking.difficulty} | {ranking.metric}\n")

    try:
        print(await client.get_rate_info(), "\n")

        # rateLimitData: two readings in a row
        costs = []
        for _ in range(repeats):
            first = await points_spent(client)
            costs.append(await points_spent(client) - first)
        report("rateLimitData", costs)

        # rankings query: page 1, as a Refresh asks for it
        rankings: list[wcl.CharacterRanking] = []

        async def load_rankings() -> None:
            result = wcl.Query.model_validate(await client.query(loader.get_query()))
            rankings[:] = result.world_data.encounter.characterRankings.rankings

        report("characterRankings", [await measure(client, load_rankings) for _ in range(repeats)])

        reports = [r for r in map(loader._ranking_to_report, rankings) if r]  # ruff: ignore[private-member-access]
        for spec_report in reports:
            spec_report.post_init()  # links fights, players and bosses to their parents, like a Refresh
        if len(reports) < 2 * repeats + 1:
            raise SystemExit(f"only {len(reports)} reports in the ranking, need {2 * repeats + 1}")

        # per report, as a Refresh loads a new one: fight phases + the ranked player's casts
        costs = []
        for spec_report in reports[:repeats]:
            costs.append(await measure(client, lambda r=spec_report: loader._load_report(r, game_data, client, None)))  # ruff: ignore[private-member-access]
        report("report: phases + player", costs)

        # boss of the top fight: once per Refresh
        top_fight = reports[repeats].fights[0]
        boss_cost = await measure(client, BossLoader(top_fight.boss, game_data).load)
        report("boss (top fight)", [boss_cost])

        # the alternative: every event of the fight, unfiltered (other reports, so no cache helps)
        costs, sizes = [], []
        for event_report in reports[repeats + 1 : 2 * repeats + 1]:
            fight = event_report.fights[0]

            async def load_events(code: str = event_report.report_id, fight_id: int = fight.fight_id) -> None:
                sizes.append(await fight_events(client, code, fight_id))

            costs.append(await measure(client, load_events))
        pages = ", ".join(f"{p}p/{e}ev" for p, e in sizes)
        report("whole-fight events", costs, f"({pages})")
    finally:
        await client.session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-version", default="retail", choices=sorted(GAME_VERSIONS))
    parser.add_argument("--spec", default="mage-frost")
    parser.add_argument("--boss", default="", help="defaults to the first boss of the current season")
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args()
    asyncio.run(main(args.game_version, args.spec, args.boss, args.repeats))
