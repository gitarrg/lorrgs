#!/usr/bin/env python

"""Small utility script to:
- remove any old reports without phase-data
- load the new "top report"'s boss casts to fill

"""


import asyncio
import itertools
import dotenv
import logging

from lorgs import utils
from lorgs.clients.wcl.models import query
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_report import Report

dotenv.load_dotenv()

# IMPORT LOCAL LIBRARIES
from lorgs.clients import sqs, wcl
from lorgs.models.wow_spec import WowSpec
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.warcraftlogs_ranking import SpecRanking

# data
from lorgs.data.classes import *
from lorgs.data.expansions.the_war_within.raids.undermine import *


log = logging.getLogger()
log.setLevel(logging.DEBUG)


async def fix_spec_ranking(
    spec: WowSpec,
    boss: RaidBoss,
    difficulty: str = "mythic",
    metric: str = "dps",
) -> None:

    print(f"[Fixing] {spec.full_name} {boss.full_name_slug} {difficulty} {metric}")

    spec_ranking = SpecRanking.get(
        spec_slug=spec.full_name_slug,
        boss_slug=boss.full_name_slug,
        difficulty=difficulty,
        metric=metric,
    )
    if not spec_ranking:
        log.warning(f"SpecRanking not found for {spec.full_name} {boss.full_name_slug} {difficulty} {metric}")
        return

    # Check if its already fixed
    missing = [report for report in spec_ranking.reports if not report.region]
    if len(missing) <= 3:
        print("Already fixed")
        return

    reports_by_id: dict[str, Report] = {}

    for report in spec_ranking.reports:
        reports_by_id[report.report_id] = report

    query = spec_ranking.get_query()
    query_result = await spec_ranking.client.query(query, raise_errors=False)

    query_result = query_result["worldData"]
    world_data = wcl.WorldData(**query_result)
    rankings = world_data.encounter.characterRankings.rankings

    for ranking in rankings:

        report_data = ranking.report
        if not report_data:
            continue

        report = reports_by_id.get(report_data.code)
        if not report:
            continue

        if ranking.server and ranking.server.region:
            report.region = ranking.server.region
            print(report.report_id, "region", report.region)

    """
    # print("================")
    # print(queries)
    # return

    for report, result in zip(spec_ranking.reports, results):
        if not result:
            continue

        region = utils.get_nested_key(result, ["reportData", "report", "region", "slug"])
        print(report.report_id, "region", region)
        if region:
            report.region = region
    """

    spec_ranking.save()


async def main() -> None:
    print("main")

    bosses = [
        VEXIE,
        CAULDRON,
        RIK,
        STIX,
        LOCKENSTOCK,
        ONE_ARMED_BANDIT,
        MUGZEE,
        GALLYWIX,
    ]

    specs = [
        *DEATHKNIGHT.specs,
        *DEMONHUNTER.specs,
        *DRUID.specs,
        *EVOKER.specs,
        *HUNTER.specs,
        *MAGE.specs,
        *MONK.specs,
        *PALADIN.specs,
        *PRIEST.specs,
        *ROGUE.specs,
        *SHAMAN.specs,
        *WARLOCK.specs,
        *WARRIOR.specs,
    ]

    # import sys
    # class_name = sys.argv[1]
    # class_ = WowClass.get(name=class_name)
    # # print(class_)
    # specs = class_.specs
    difficulties = ["mythic"]  # , "heroic"]
    metrics = ["dps", "hps", "bossdps"]

    for spec, boss, difficulty, metric in itertools.product(specs, bosses, difficulties, metrics):
        await fix_spec_ranking(spec, boss, difficulty, metric)
        # print("sleeping 30 seconds")
        # await asyncio.sleep(30)

    print("done")


if __name__ == "__main__":
    asyncio.run(main())
