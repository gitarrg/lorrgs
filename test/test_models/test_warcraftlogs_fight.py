import datetime
import unittest

from lorgs.clients import wcl
from lorgs.loaders.fight_loader import FightLoader
from lorgs.models.warcraftlogs_comp_ranking import get_composition
from lorgs.models.warcraftlogs_fight import Fight

from ..helpers import load_fixture


def _fight(**kwargs) -> Fight:
    values = {
        "fight_id": 5,
        "start_time": datetime.datetime.fromtimestamp(101, datetime.UTC),
        "duration": 3000,
    }
    values.update(kwargs)
    return Fight(**values)


class TestFight(unittest.TestCase):
    def setUp(self):
        self.fight = _fight()
        self.fight.report = unittest.mock.MagicMock()
        self.fight.report.start_time = datetime.datetime.fromtimestamp(100, datetime.UTC)
        self.fight.report.report_id = "REPORT_ID"

    def test_start_time_rel(self):
        self.fight.report.start_time = datetime.datetime.fromtimestamp(100, datetime.UTC)
        self.fight.start_time = datetime.datetime.fromtimestamp(121, datetime.UTC)
        assert self.fight.start_time_rel == 21000

    def test_end_time_rel(self):
        self.fight.report.start_time = datetime.datetime.fromtimestamp(100, datetime.UTC)
        self.fight.start_time = datetime.datetime.fromtimestamp(120, datetime.UTC)
        self.fight.duration = 600 * 1000
        assert self.fight.end_time_rel == 620 * 1000

    def test_table_query_args(self):
        result = self.fight.table_query_args
        assert result == "fightIDs: 5, startTime: 1000, endTime: 4000"


class TestFightProcessPlayers(unittest.TestCase):
    def setUp(self):
        self.fight = _fight()
        self.loader = FightLoader(self.fight)

    def test_empty(self):
        self.loader._process_summary(wcl.ReportSummary())
        assert self.fight.players == []

    def test_valid_player(self):
        import lorgs.data  # noqa: F401

        summary = wcl.ReportSummary(
            composition=[
                {
                    "id": 1,
                    "name": "Some Player",
                    "type": "Druid",
                    "specs": [{"spec": "Restoration"}],
                },
                {
                    "id": 2,
                    "name": "Other Player",
                    "type": "DemonHunter",
                    "specs": [{"spec": "Vengeance"}],
                },
            ],
        )
        self.loader._process_summary(summary)

        assert len(self.fight.players) == 2

        player1 = self.fight.get_player(source_id=1)
        assert player1 is not None
        assert player1.name == "Some Player"
        assert player1.spec_slug == "druid-restoration"

        player2 = self.fight.get_player(source_id=2)
        assert player2 is not None
        assert player2.name == "Other Player"
        assert player2.spec_slug == "demonhunter-vengeance"

    def test_example_fixture(self):
        import lorgs.data  # noqa: F401

        self.fight.duration = 0
        fight_data = load_fixture("fight_summary_1.json")
        self.loader.process_query_result(fight_data["data"]["reportData"])

        assert len(self.fight.players) == 20
        assert self.fight.duration == 728598

        comp = get_composition(self.fight.players)
        assert comp["roles"]["tank"] == 2
        assert comp["roles"]["heal"] == 4
        assert comp["specs"]["hunter-marksmanship"] == 2
        assert comp["specs"]["monk-windwalker"] == 1
        assert comp["classes"]["warlock"] == 2

        player_arrg = self.fight.get_player(source_id=17)
        assert player_arrg is not None
        assert player_arrg.name == "Arrg"
        assert player_arrg.spec_slug == "druid-restoration"
        assert player_arrg.total == 10761
