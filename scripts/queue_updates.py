#!/usr/bin/env python

"""
PYTHONPATH=. uv run --env-file=.env scripts/queue_updates.py




"""


# IMPORT LOCAL LIBRARIES
import asyncio
from lorgs.clients import sqs
from lorgs.data.classes import *

from lorgs.models.task_payloads import CompRankingPayload, SpecRankingPayload
from lorgs.models.wow_spec import WowSpec
from lorgs.models.raid_boss import RaidBoss

from lorgs.data.season import CURRENT_SEASON
from lorgs.data.expansions.midnight.raids import (
    VOIDSPIRE,
    DREAMRIFT,
    MARCH_ON_QUALDANAS,
)

from lorgs.data.expansions.midnight.raids.voidspire import (
    AVERZIAN,
    FALLEN_KING_SALHADAAR,
    LIGHTBLINDED_VANGUARD,
    VORASIUS,
    VAELGOR_EZZORAK,
    CROWN_OF_THE_COSMOS,
)


async def load_remote(
    spec: WowSpec,
    boss: RaidBoss,
    difficulty="all",
    metric="all",
    limit=50,
    *,
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


async def load_local(
    spec: WowSpec,
    boss: RaidBoss,
    difficulty: str = "mythic",
    metric: str = "",
    limit=50,
    clear: bool = False,
):
    import asyncio
    from lorgs.clients.wcl import WarcraftlogsClient
    from lorgs.loaders.spec_ranking import SpecRankingLoader
    from lorgs.models.warcraftlogs_ranking import SpecRanking

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


async def load_spec_rankings() -> None:
    bosses = [
        *VOIDSPIRE.bosses,
        *DREAMRIFT.bosses,
        *MARCH_ON_QUALDANAS.bosses,
    ]

    specs: list[WowSpec] = [
        # DK
        # DEATHKNIGHT_BLOOD,
        # DEATHKNIGHT_FROST,
        # DEATHKNIGHT_UNHOLY,

        # DH
        # DEMONHUNTER_HAVOC,
        # DEMONHUNTER_VENGEANCE,
        # DEMONHUNTER_DEVOURER,

        # Druid
        # DRUID_BALANCE,
        # DRUID_FERAL,
        # DRUID_GUARDIAN,
        # DRUID_RESTORATION,

        # Evoker
        # EVOKER_AUGMENTATION,
        # EVOKER_DEVASTATION,
        # EVOKER_PRESERVATION,

        # Hunter
        # HUNTER_BEASTMASTERY,
        # HUNTER_MARKSMANSHIP,
        # HUNTER_SURVIVAL,

        # Mage
        # MAGE_ARCANE,
        # MAGE_FIRE,
        # MAGE_FROST,

        # Monk
        # MONK_BREWMASTER,
        # MONK_MISTWEAVER,
        # MONK_WINDWALKER,

        # Priest
        # PRIEST_DISCIPLINE,
        # PRIEST_HOLY,
        # PRIEST_SHADOW,

        # Paladin
        # PALADIN_HOLY,
        # PALADIN_PROTECTION,
        # PALADIN_RETRIBUTION,

        # Rogue
        # ROGUE_ASSASSINATION,
        # ROGUE_OUTLAW,
        # ROGUE_SUBTLETY,

        # Shaman
        # SHAMAN_ELEMENTAL,
        # SHAMAN_ENHANCEMENT,
        # SHAMAN_RESTORATION,

        # Warlock
        # WARLOCK_AFFLICTION,
        # WARLOCK_DESTRUCTION,
        # WARLOCK_DEMONOLOGY,

        # Warrior
        # WARRIOR_ARMS,
        # WARRIOR_FURY,
        # WARRIOR_PROTECTION,
    ]
    specs = ALL_SPECS
    # specs = HEAL.specs

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
                difficulty="mythic",
                # metric="hps",
                # limit=20,
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
        "difficulty": "mythic",
        "metric": "all",
        "limit": 50,
        "clear": False,
    }
    print("q", payload)
    return sqs.send_message(payload=payload)


if __name__ == "__main__":
    load_all()
    # asyncio.run(load_spec_rankings())
