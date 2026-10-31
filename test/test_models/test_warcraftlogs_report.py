import datetime
import unittest

from lorgs.clients import wcl
from lorgs.loaders.fight_loader import FightLoader
from lorgs.loaders.report_overview_loader import ReportOverviewLoader
from lorgs.models.warcraftlogs_player import Player
from lorgs.models.warcraftlogs_report import Report
from test.helpers import game_data_with, report_query


class TestReport(unittest.TestCase):
    def setUp(self) -> None:
        self.report = Report(
            report_id="REPORT_ID",
            start_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.UTC),
        )
        self.loader = ReportOverviewLoader(self.report, game_data_with())

    def test_get_query(self):
        assert "REPORT_ID" in self.loader.get_query()

    def test_process_query_result_title(self):
        self.loader.process_query_result(report_query(title="new title"))
        assert self.report.title == "new title"

    def test_process_query_result_start_time(self):
        start_time = datetime.datetime(2024, 5, 1, tzinfo=datetime.UTC)
        self.loader.process_query_result(report_query(startTime=start_time))
        assert self.report.start_time == start_time

    def test_process_query_result_zone_id_valid(self):
        self.loader.process_query_result(report_query(zone={"id": 42}))
        assert self.report.zone_id == 42

    def test_process_query_result_zone_id_missing(self):
        self.loader.process_query_result(report_query())
        assert self.report.zone_id == -1

    def test_process_master_data_clears_players(self):
        self.report.players = [Player(source_id=1, name="old")]
        self.loader._process_master_data(wcl.ReportMasterData(actors=[]))
        assert self.report.players == []

    def test_fight_from_wcl_fight_skips_trash(self):
        fight = FightLoader.fight_from_wcl_fight(wcl.ReportFight(id=1, encounterID=0), self.report, game_data_with())
        assert fight is None

    def test_fight_from_wcl_fight_basic(self):
        fight = FightLoader.fight_from_wcl_fight(
            wcl.ReportFight(
                id=10,
                encounterID=2407,
                fightPercentage=70.99,
                kill=False,
                startTime=400000,
                endTime=500000,
            ),
            self.report,
            game_data_with(),
        )
        assert fight is not None
        assert fight.percent == 70.99
        assert fight.kill is False
        assert fight.duration == 100001
        assert fight.start_time == self.report.start_time + datetime.timedelta(milliseconds=400000)
