#!/usr/bin/env python

"""
PYTHONPATH=. uv run --env-file=.env scripts/queue_updates.py




"""


# IMPORT LOCAL LIBRARIES
from lorgs.clients import sqs
from lorgs.data.classes import *

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


def load_remote(
    spec: WowSpec,
    boss: RaidBoss,
    difficulty="all",
    metric="all",
    limit=50,
    clear: bool = False,
):
    payload = {
        "task": "load_spec_rankings",
        "spec_slug": spec.full_name_slug,
        "boss_slug": boss.full_name_slug,
        "difficulty": difficulty,
        "metric": metric,
        "limit": limit,
        "clear": clear,
    }

    # print(payload)
    # from lorrgs_sqs import helpers
    # for pl in helpers.expand_keywords(payload):
    #     print(pl)
    return sqs.send_message(payload=payload)


def load_local(
    spec: WowSpec,
    boss: RaidBoss,
    difficulty: str = "mythic",
    metric: str = "dps",
    limit=50,
    clear: bool = False,
):
    import asyncio
    from lorgs.models.warcraftlogs_ranking import SpecRanking

    spec_ranking = SpecRanking.get_or_create(
        spec_slug=spec.full_name_slug,
        boss_slug=boss.full_name_slug,
        difficulty=difficulty,
        metric=metric,
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(spec_ranking.load(limit=limit, clear_old=clear))

    spec_ranking.save()


def load_spec_rankings() -> None:
    bosses = [
        *VOIDSPIRE.bosses,
        *DREAMRIFT.bosses,
        # *MARCH_ON_QUALDANAS.bosses,
        #' CROWN_OF_THE_COSMOS,
    ]

    specs: list[WowSpec] = [
        MONK_WINDWALKER,
        # DRUID_BALANCE,
        # SHAMAN_ELEMENTAL,
        # SHAMAN_RESTORATION,
        # MONK_MISTWEAVER,
        # WARLOCK_DESTRUCTION,
        # WARLOCK_AFFLICTION,
        # WARLOCK_DEMONOLOGY,
        # HUNTER_BEASTMASTERY,
        # HUNTER_MARKSMANSHIP,
        # HUNTER_SURVIVAL,
        # MAGE_ARCANE,
        # MAGE_FIRE,
        # MAGE_FROST,
        # EVOKER_AUGMENTATION,
        # EVOKER_PRESERVATION,
        # DEMONHUNTER_HAVOC,
        # PRIEST_SHADOW,
        # SHAMAN_RESTORATION,
        # SHAMAN_ELEMENTAL,
        # SHAMAN_ENHANCEMENT
        # PRIEST_HOLY
        # MAGE_ARCANE,
        # PALADIN_HOLY,
        # MONK_WINDWALKER,
        # *MDPS.specs,
        # *RDPS.specs,
    ]
    # specs = ALL_SPECS
    # specs = HEAL.specs

    # load = load_remote
    load = load_local

    for spec in specs:
        print(spec.full_name_slug)
        for boss in bosses:
            print("\t", boss.full_name_slug)

            load(
                spec,
                boss,
                clear=True,
                difficulty="heroic",
                metric="dps",
            )


def load_comp_ranking(boss_slug: str = "all"):
    payload = {
        "task": "load_comp_rankings",
        "boss_slug": boss_slug,
    }
    print("q", payload)
    return sqs.send_message(payload=payload)


if __name__ == "__main__":
    # load_spec_rankings()

    # load_remote()
    # load_comp_ranking()

    payload = {
        "task": "load_spec_rankings",
        "spec_slug": "all",
        "boss_slug": "all",
        "difficulty": "mythic",
        "metric": "all",
        "limit": 25,
        "clear": False,
    }
    print("q", payload)
    sqs.send_message(payload=payload)
