#!/usr/bin/env python

import dotenv

dotenv.load_dotenv()

# IMPORT LOCAL LIBRARIES
from lorgs.clients import sqs
from lorgs.data.classes import *

from lorgs.models.wow_spec import WowSpec
from lorgs.models.raid_boss import RaidBoss

from lorgs.data.season import CURRENT_SEASON
from lorgs.data.expansions.the_war_within.raids.manaforge_omaga import MANAFORGE_OMEGA


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
        # BLOODBOUND_HORROR
        # ANSUREK,
        # OVINAX,
        # ULGRAX,
    ]
    bosses = MANAFORGE_OMEGA.bosses

    specs = [
        # DRUID_BALANCE,
        SHAMAN_ELEMENTAL,
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
    # specs = DPS.specs

    load = load_remote
    load = load_local

    for spec in specs:
        print(spec.full_name_slug)
        for boss in bosses:
            print("\t", boss.full_name_slug)

            load(
                spec,
                boss,
                clear=True,
                difficulty="mythic",
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
    load_spec_rankings()
    # load_comp_ranking()
