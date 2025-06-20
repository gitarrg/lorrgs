#!/usr/bin/env python

import dotenv

from lorgs.data.expansions.the_war_within.raids.undermine import *
from lorgs.data.season import CURRENT_SEASON

dotenv.load_dotenv()

# IMPORT LOCAL LIBRARIES
from lorgs.clients import sqs
from lorgs.models.wow_spec import WowSpec
from lorgs.models.raid_boss import RaidBoss

# data
from lorgs.data.classes import *
from lorgs.data.expansions.the_war_within.raids.nerubar_palace import *


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
        # VEXIE,
        # CAULDRON,
        # RIK,
        # STIX,
        LOCKENSTOCK,
        # ONE_ARMED_BANDIT,
        # MUGZEE,
        # GALLYWIX,
    ]

    # bosses = LIBERATION_OF_UNDERMINE.bosses

    specs = [
        # *HEAL.specs,
        # *RDPS.specs,
        # *MDPS.specs,
        # DRUID_FERAL,
        WARLOCK_DESTRUCTION,
        # WARRIOR_ARMS,
        # MONK_MISTWEAVER,
        # PRIEST_DISCIPLINE,
        # SHAMAN_ENHANCEMENT,
        # PALADIN_RETRIBUTION,
    ]
    # specs = ALL_SPECS

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
                difficulty="normal",
                # metric="hps",
                limit=10,
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
