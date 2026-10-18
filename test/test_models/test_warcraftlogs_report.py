import datetime
import unittest

import lorgs.data  # noqa: F401
from lorgs.clients import wcl
from lorgs.loaders.fight_loader import FightLoader
from lorgs.loaders.report_overview_loader import ReportOverviewLoader
from lorgs.models.warcraftlogs_player import Player
from lorgs.models.warcraftlogs_report import Report


class TestReport(unittest.TestCase):
    def setUp(self) -> None:
        self.report = Report(
            report_id="REPORT_ID",
            start_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.UTC),
        )
        self.loader = ReportOverviewLoader(self.report)

    def test_get_query(self):
        assert "REPORT_ID" in self.loader.get_query()

    def test_process_query_result_title(self):
        self.loader.process_query_result({"report": {"title": "new title"}})
        assert self.report.title == "new title"

    def test_process_query_result_start_time(self):
        start_time = datetime.datetime(2024, 5, 1, tzinfo=datetime.UTC)
        self.loader.process_query_result({"report": {"startTime": start_time}})
        assert self.report.start_time == start_time

    def test_process_query_result_zone_id_valid(self):
        self.loader.process_query_result({"report": {"zone": {"id": 42}}})
        assert self.report.zone_id == 42

    def test_process_query_result_zone_id_missing(self):
        self.loader.process_query_result({"report": {}})
        assert self.report.zone_id == -1

    def test_process_master_data_clears_players(self):
        self.report.players = [Player(source_id=1, name="old")]
        self.loader._process_master_data(wcl.ReportMasterData(actors=[]))
        assert self.report.players == []

    def test_player_from_actor_data(self):
        actor = wcl.ReportActor(
            id=32,
            name="PlayerName",
            icon="Shaman-Restoration",
            type="Player",
            subType="Shaman",
        )
        player = self.loader._player_from_actor_data(actor)
        assert player is not None
        assert player.source_id == 32
        assert player.name == "PlayerName"
        assert player.spec_slug == "shaman-restoration"
        assert player.class_slug == "shaman"

    def test_player_from_actor_data_unknown_spec(self):
        actor = wcl.ReportActor(id=5, name="HunterPlayer", icon="Hunter", subType="Hunter")
        player = self.loader._player_from_actor_data(actor)
        assert player is not None
        assert player.spec_slug == ""
        assert player.class_slug == "hunter"

    def test_fight_from_wcl_fight_skips_trash(self):
        fight = FightLoader.fight_from_wcl_fight(wcl.ReportFight(id=1, encounterID=0), self.report)
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
        )
        assert fight is not None
        assert fight.percent == 70.99
        assert fight.kill is False
        assert fight.duration == 100001
        assert fight.start_time == self.report.start_time + datetime.timedelta(milliseconds=400000)
