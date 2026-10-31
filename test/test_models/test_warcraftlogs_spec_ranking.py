# IMPORT STANDARD LIBRARIES
import unittest
from unittest import mock

import pytest


# IMPORT LOCAL LIBRARIES
from lorgs.clients import wcl
from lorgs.loaders.spec_ranking import SpecRankingLoader
from lorgs.models.warcraftlogs_ranking import SpecRanking
from ..helpers import load_fixture


class TestSpecRankingLoader(unittest.TestCase):
    def setUp(self) -> None:
        self.spec_ranking = SpecRanking(
            game_version="retail", spec_slug="test-spec", boss_slug="test-boss", difficulty="mythic", metric="dps"
        )
        boss = mock.MagicMock(id=2048)
        spec = mock.MagicMock(**{
            "wow_class.name_slug_cap": "ClassName",
            "name_slug_cap": "SpecName",
            "role.metric": "dps",
        })
        game_data = mock.MagicMock()
        game_data.get_boss.return_value = boss
        game_data.get_spec.return_value = spec
        game_version = mock.MagicMock()
        game_version.name = "retail"
        game_version.data = game_data
        self.loader = SpecRankingLoader(self.spec_ranking, game_version)

    def test__get_query(self):
        query = self.loader.get_query()

        assert 'className: "ClassName"' in query
        assert 'specName: "SpecName"' in query
        assert "metric: dps" in query

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
                                "report": {"code": "REPORT_CODE", "fightID": 5, "startTime": 1634543354962},
                            }
                        ]
                    }
                }
            }
        }
        self.loader.process_query_result(wcl.Query.model_validate(data))

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

        self.loader.process_query_result(wcl.Query.model_validate(data))

        assert len(self.spec_ranking.reports) == 10


def test_loader_rejects_a_ranking_of_another_game_version() -> None:
    from lorgs.data import MISTS, RETAIL

    ranking = SpecRanking(game_version="mists", spec_slug="mage-fire", boss_slug="b", difficulty="heroic", metric="dps")
    with pytest.raises(ValueError, match="belongs to Game Version 'mists', not 'retail'"):
        SpecRankingLoader(ranking, RETAIL)
    assert SpecRankingLoader(ranking, MISTS).game_data is MISTS.data
