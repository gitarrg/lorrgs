#!/usr/bin/env -S PYTHONPATH=. uv run uv run --env-file=.env
"""Manually load spec rankings for a given spec and boss.

>>> PYTHONPATH=. uv run --env-file=.env scripts/queue_updates.py [boss_slug ...]

"""
# IMPORT STANDARD LIBRARIES
import asyncio
import sys

# IMPORT LOCAL LIBRARIES
from lorgs.clients import sqs
from lorgs.game_version import ACTIVE
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.task_payloads import SpecRankingPayload
from lorgs.models.wow_spec import WowSpec
from lorrgs_sqs.helpers import ALL_BOSSES, ALL_SPECS


async def load_remote(  # ruff: ignore[too-many-arguments, unused-async]
    spec: WowSpec,
    boss: RaidBoss,
    difficulty="all",
    metric="all",
    *,
    limit=50,
    clear: bool = False,
):
    payload = SpecRankingPayload(
        spec_slug=spec.full_name_slug,
        boss_slug=boss.full_name_slug,
        difficulty=difficulty,
        metric=metric,
        limit=limit,
        clear=clear,
    )
    return sqs.send_message(payload=payload)


async def load_local(  # ruff: ignore[too-many-arguments]
    spec: WowSpec,
    boss: RaidBoss,
    difficulty: str = ACTIVE.default_difficulty_name,
    metric: str = "",
    *,
    limit: int = 50,
    clear: bool = False,
):
    # ruff: disable[import-outside-top-level]
    from lorgs.clients.wcl import WarcraftlogsClient
    from lorgs.loaders.spec_ranking import SpecRankingLoader
    from lorgs.models.warcraftlogs_ranking import SpecRanking
    # ruff: enable[import-outside-top-level]

    if not metric:
        metric = spec.role.metric

    spec_ranking = SpecRanking.get_or_create(
        spec_slug=spec.full_name_slug,
        boss_slug=boss.full_name_slug,
        difficulty=difficulty,
        metric=metric,
    )

    client = WarcraftlogsClient.get_instance()
    await SpecRankingLoader(spec_ranking).load(client, limit=limit, clear_old=clear)

    spec_ranking.save()


async def load_spec_rankings(boss_slugs: list[str]) -> None:
    # all bosses of the current Season, or only the given boss slugs
    bosses = [boss for boss in ALL_BOSSES if not boss_slugs or boss.full_name_slug in boss_slugs]
    specs: set[WowSpec] = {*ALL_SPECS}

    load = load_remote
    # load = load_local

    for spec in specs:
        print(spec.full_name_slug)
        for boss in bosses:
            print("\t", boss.full_name_slug)

            await load(
                spec,
                boss,
                clear=True,
                difficulty=ACTIVE.default_difficulty_name,
                # metric="dps",
                limit=35,
            )


def load_comp_ranking(boss_slug: str = "all"):
    payload = {
        "task": "load_comp_rankings",
        "boss_slug": boss_slug,
    }
    print("q", payload)
    return sqs.send_message(payload=payload)


def load_all():
    payload = {
        "task": "load_spec_rankings",
        "spec_slug": "all",
        "boss_slug": "all",
        "difficulty": ACTIVE.default_difficulty_name,
        "metric": "all",
        "limit": 50,
        "clear": False,
    }
    print("q", payload)
    return sqs.send_message(payload=payload)


if __name__ == "__main__":
    # load_all()
    asyncio.run(load_spec_rankings(sys.argv[1:]))
