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


################################################################################
# Talents
#


def _talent_loader(*, has_talents: bool) -> SpecRankingLoader:
    ranking = SpecRanking(game_version="retail", spec_slug="s", boss_slug="b", difficulty="mythic", metric="dps")
    game_version = mock.MagicMock(has_talents=has_talents)
    game_version.name = "retail"
    return SpecRankingLoader(ranking, game_version)


def _ranking_data(talents: list[dict] | None = None) -> wcl.Query:
    entry: dict = {
        "name": "PlayerName",
        "class": "Paladin",
        "spec": "Holy",
        "amount": 1,
        "duration": 1,
        "startTime": 1634544096374,
        "report": {"code": "CODE", "fightID": 5, "startTime": 1634543354962},
    }
    if talents is not None:
        entry["talents"] = talents
    return wcl.Query.model_validate({"worldData": {"encounter": {"characterRankings": {"rankings": [entry]}}}})


def test_talents_are_stored_compact() -> None:
    loader = _talent_loader(has_talents=True)
    loader.process_query_result(
        _ranking_data([{"talentID": 100, "points": 1}, {"talentID": 101, "points": 2}, {"talentID": 102}])
    )

    player = loader.ranking.players[0]
    assert player.talents == [100, (101, 2), 102]
    assert '"talents":[100,[101,2],102]' in player.model_dump_json(exclude_unset=True)


def test_player_without_talents_has_none() -> None:
    loader = _talent_loader(has_talents=True)
    loader.process_query_result(_ranking_data())
    assert loader.ranking.players[0].talents == []


def test_talents_are_skipped_without_game_version_support() -> None:
    loader = _talent_loader(has_talents=False)
    loader.process_query_result(_ranking_data([{"talentID": 100, "points": 1}]))
    assert loader.ranking.players[0].talents == []


def test_query_requests_combatant_info_only_with_talents() -> None:
    for has_talents in (True, False):
        loader = _talent_loader(has_talents=has_talents)
        loader.game_data.get_boss.return_value = mock.MagicMock(id=1)
        loader.game_data.get_spec.return_value = mock.MagicMock(**{
            "wow_class.name_slug_cap": "C",
            "name_slug_cap": "S",
        })
        assert f"includeCombatantInfo: {str(has_talents).lower()}" in loader.get_query()


def test_refresh_backfills_talents_without_touching_casts() -> None:
    loader = _talent_loader(has_talents=True)
    loader.process_query_result(_ranking_data())  # stored before Talents existed
    player = loader.ranking.players[0]
    player.casts = [mock.sentinel.cast]  # stands in for already loaded casts

    loader.process_query_result(_ranking_data([{"talentID": 100, "points": 3}]))

    assert len(loader.ranking.players) == 1
    assert loader.ranking.players[0] is player
    assert player.talents == [(100, 3)]
    assert player.casts == [mock.sentinel.cast]
    assert "talents" in player.model_fields_set
