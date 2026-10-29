"""Players of a Fight summary are matched to Retail specs."""

import unittest

from lorgs.data import GAME_DATA
from lorgs.clients import wcl
from lorgs.loaders.fight_loader import FightLoader
from lorgs.models.warcraftlogs_comp_ranking import get_composition
from lorgs.models.warcraftlogs_report import Report
from test.helpers import load_fixture
from test.test_models.test_warcraftlogs_fight import _fight


class TestFightProcessPlayers(unittest.TestCase):
    def setUp(self):
        self.fight = _fight()
        # Deaths convert through the Fight, which needs its Report.
        self.fight.report = Report(report_id="REPORT_ID", start_time=self.fight.start_time)
        self.loader = FightLoader(self.fight)

    def test_valid_player(self):
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
        self.fight.duration = 0
        fight_data = load_fixture("fight_summary_1.json")
        self.loader.process_query_result(fight_data["data"]["reportData"])

        assert len(self.fight.players) == 20
        assert self.fight.duration == 728598

        comp = get_composition(self.fight.players, GAME_DATA)
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
