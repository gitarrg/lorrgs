# IMPORT STANDARD LIBRARIES
import unittest
from unittest import mock


# IMPORT LOCAL LIBRARIES
from lorgs.loaders.spec_ranking import SpecRankingLoader
from lorgs.models.warcraftlogs_ranking import SpecRanking
from ..helpers import load_fixture


class TestSpecRankingLoader(unittest.TestCase):


    def setUp(self) -> None:
        self.spec_ranking = SpecRanking(spec_slug="test-spec", boss_slug="test-boss", metric="dps")
        self.loader = SpecRankingLoader(self.spec_ranking)

        self.boss_patch = mock.patch("lorgs.models.raid_boss.RaidBoss.get")
        self.boss_mock = self.boss_patch.start()
        self.boss_mock.return_value = mock.MagicMock(id=2048)


        self.spec_patch = mock.patch("lorgs.models.wow_spec.WowSpec.get")
        self.spec_mock = self.spec_patch.start()
        self.spec_mock.return_value = mock.MagicMock(**{
            "wow_class.name_slug_cap": "ClassName",
            "name_slug_cap": "SpecName",
            "role.metric": "dps",
        })

    def tearDown(self) -> None:
        self.boss_patch.stop()
        self.spec_patch.stop()


    def test__get_query(self):
        query = self.loader.get_query()

        assert 'className: "ClassName"' in query
        assert 'specName: "SpecName"' in query
        assert 'metric: dps' in query

    def test__process_query_result_one(self):

        data = {
            "worldData": {
                "encounter": {
                    "characterRankings": {
                        "rankings": [
                            {
                                "name": "PlayerName",
                                "class": "Warrior",
                                "spec": "Arms",
							    "amount": 123456,
							    "duration": 5432,
							    "startTime": 1634544096374,
							    "report": {
								    "code": "REPORT_CODE",
								    "fightID": 5,
								    "startTime": 1634543354962
							    }
                            }
                        ]
                    }
                }
            }
        }
        self.loader.process_query_result(data)

        assert len(self.spec_ranking.reports) == 1

        report = self.spec_ranking.reports[0]
        assert report.report_id == "REPORT_CODE"

        fight = report.fights[0]
        assert fight.fight_id == 5
        assert fight.duration == 5432

        player = fight.players[0]
        assert player.name == "PlayerName"
        assert player.total == 123456
        assert player.casts == []

    def test__process_query_result_fixture(self):

        data = load_fixture("spec_rankings_1.json")

        self.loader.process_query_result(data)

        assert len(self.spec_ranking.reports) == 10
