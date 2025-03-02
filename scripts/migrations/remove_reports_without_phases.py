#!/usr/bin/env python

"""Small utility script to:
- remove any old reports without phase-data
- load the new "top report"'s boss casts to fill

"""


import asyncio
import dotenv
import logging

from lorgs.data.season import CURRENT_SEASON
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_report import Report

dotenv.load_dotenv()

# IMPORT LOCAL LIBRARIES
from lorgs.clients import sqs
from lorgs.models.wow_spec import WowSpec
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.warcraftlogs_ranking import SpecRanking

# data
from lorgs.data.classes import *
from lorgs.data.expansions.the_war_within.raids.nerubar_palace import *


log = logging.getLogger()
log.setLevel(logging.DEBUG)


def fight_has_phases(fight: Fight) -> bool:
    return bool(fight.phases)


def report_has_phases(report: Report):
    return all(fight_has_phases(fight) for fight in report.fights)


async def load_top_report(ranking: SpecRanking) -> None:

    try:
        fight = ranking.fights[0]
    except IndexError:
        return

    boss = fight.boss
    if not boss:
        return

    # if len(boss.casts) > 5:
    #     return

    print("loading", ranking.spec_slug, ranking.boss_slug, ranking.difficulty, ranking.metric)

    boss.query_mode = boss.QueryModes.ALL
    # boss.casts = []
    # boss.phases = []  # reset these, otherwise we'll just append again
    # boss.casts = boss.casts[:]  # not sure if required

    await boss.load()
    ranking.save()


async def main() -> None:

    for raid in CURRENT_SEASON.raids:
        # for boss in raid.bosses:
        for boss in [RASHANAN, OVINAX]:

            if not boss.phases:
                log.info(f"Skipping {boss.full_name_slug}")
                continue

            log.info(f"Process: {boss.full_name_slug}")

            for spec in sorted(list(ALL_SPECS)):
                for difficulty in ["mythic"]:  # "heroic",
                    for metric in spec.role.metrics:

                        spec_ranking = SpecRanking.get_or_create(
                            spec_slug=spec.full_name_slug,
                            boss_slug=boss.full_name_slug,
                            difficulty=difficulty,
                            metric=metric,
                        )

                        reports_without_phase = [r for r in spec_ranking.reports if not report_has_phases(r)]
                        reports_with_phase = [r for r in spec_ranking.reports if report_has_phases(r)]
                        log.debug(f"{boss.name} | {spec.full_name_slug} {difficulty} {metric}")
                        log.debug(f"With: {len(reports_with_phase)} / Without: {len(reports_without_phase)}")

                        if reports_without_phase:
                            spec_ranking.reports = reports_with_phase
                            spec_ranking.save()
                            log.debug(f"{boss.name} | {spec.full_name_slug} {difficulty} {metric} Updated")
                            log.info(f"Kept: {len(reports_with_phase)} / Removed: {len(reports_without_phase)}")
                            # return

                        # Load first fight for each
                        await load_top_report(spec_ranking)


if __name__ == "__main__":
    asyncio.run(main())
