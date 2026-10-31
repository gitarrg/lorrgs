import dotenv
import datetime
from lorgs.clients import wcl

from lorgs.models.warcraftlogs_fight import Fight

dotenv.load_dotenv()  # pylint: disable=wrong-import-position
from lorgs import data

import asyncio
from lorgs.models.warcraftlogs_report import Report

from test import helpers


def test_load_master_fixture():

    query_result = helpers.load_fixture("report_masterData_1.json")
    query_result = query_result["data"]["reportData"]  # Make "report" the root key

    report = Report(report_id="123")
    report.process_query_result(**query_result)

    assert report.title == "Sepulcher of the First Ones"
    assert len(report.fights) == 8
    assert len(report.players) == 25


async def test_load_master_data():

    report = Report(report_id="McgBaApkj1btTWvK")

    # make sure its empty
    assert not report.title
    assert not report.players
    assert not report.fights

    # load
    await report.load()

    # make sure things are loaded
    assert report.title == "Sepulcher of the First Ones"
    assert len(report.fights) == 5, report.fights
    assert len(report.players) == 21, len(report.players)


async def test_load_fight():

    report = Report(report_id="tZVAxLYg7kTz1PBm")
    report.start_time = datetime.datetime.fromtimestamp(1666891263596 / 1000)

    fight = Fight(fight_id=2, boss_id=2553)
    fight.report = report
    fight.start_time = report.start_time + datetime.timedelta(milliseconds=271703)
    fight.end_time = report.start_time + datetime.timedelta(milliseconds=493690)

    # Update Fixture
    if False:
        q = fight.get_query()
        print(q)
        query_result = await fight.client.multiquery([q])
        query_result = query_result[0]
        print(query_result)
        helpers.save_fixture("report_data_2.json", query_result)

    query_result = helpers.load_fixture("report_data_2.json")
    # report_data = wcl.Report(**query_result)
    # print(query_result)
    # print(report_data)
    fight.process_query_result(**query_result)
    print("F", fight)
    for _, player in fight.players.items():
        print("\t", player, "Casts:", player.casts)

    # fight = report.get_fight(2)
    # await fight.load()
    # print(fight)


async def main():
    # test_load_master_fixture()
    # await test_load_master_data()
    await test_load_fight()


if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(load_casts())
