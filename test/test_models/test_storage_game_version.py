"""Seams: storage names its Game Version.

- Rankings have a `game_version` and their S3 keys start with it, for every Game Version.
- DynamoDB keys are shared between Game Versions (ADR 0003).
- A User Report records the WCL game version of its log; items without it are Retail.
"""

from __future__ import annotations

import io
from unittest import mock

import pytest

from lorgs.data import GAME_VERSIONS, MISTS, RETAIL
from lorgs.loaders.report_overview_loader import ReportOverviewLoader, UnsupportedGameVersionError
from lorgs.models.base.dynamodb import DynamoDBModel
from lorgs.models.user import User
from lorgs.models.warcraftlogs_comp_ranking import CompRanking
from lorgs.models.warcraftlogs_ranking import SpecRanking
from lorgs.models.warcraftlogs_user_report import UserReport
from test.helpers import game_data_with


SPEC_RANKING_KWARGS = {"spec_slug": "mage-fire", "boss_slug": "some-boss", "difficulty": "mythic", "metric": "dps"}


################################################################################
# S3 keys
#


@pytest.mark.parametrize("game_version", ["retail", "mists", "forever"])
def test_s3_keys_start_with_the_game_version(game_version: str) -> None:
    season_slug = GAME_VERSIONS[game_version].data.season.slug
    assert (
        SpecRanking.get_key(game_version=game_version, **SPEC_RANKING_KWARGS)
        == f"{game_version}/spec_ranking/{season_slug}/mage-fire/some-boss__mythic__dps"
    )
    assert (
        CompRanking.get_key(game_version=game_version, boss_slug="some-boss")
        == f"{game_version}/comp_ranking/some-boss"
    )


def test_game_version_is_required() -> None:
    with pytest.raises(ValueError, match="game_version"):
        SpecRanking(**SPEC_RANKING_KWARGS)
    with pytest.raises(ValueError, match="game_version"):
        CompRanking(boss_slug="some-boss")


def test_save_and_get_use_the_prefixed_key() -> None:
    ranking = SpecRanking(game_version="retail", **SPEC_RANKING_KWARGS)
    expected_key = f"retail/spec_ranking/{RETAIL.data.season.slug}/mage-fire/some-boss__mythic__dps"

    with mock.patch("lorgs.models.base.s3.s3client") as s3client:
        ranking.save()
        assert s3client.put_object.call_args.kwargs["Key"] == expected_key

        s3client.get_object.return_value = {"Body": io.BytesIO(ranking.model_dump_json().encode())}
        SpecRanking.get(game_version="retail", **SPEC_RANKING_KWARGS)
        assert s3client.get_object.call_args.kwargs["Key"] == expected_key


################################################################################
# DynamoDB keys stay shared
#


def test_dynamodb_keys_are_not_prefixed() -> None:
    assert UserReport.get_keys(report_id="abc") == {"pk": "abc", "sk": "overview"}
    assert User.get_keys(discord_id="123")["pk"] == "123"


################################################################################
# UserReport.game_version
#


def test_old_user_report_items_load_as_retail() -> None:
    """Items stored before the attribute existed have no `game_version`."""
    item = {"pk": "abc", "sk": "overview", "report_id": "abc", "title": "old"}
    report = UserReport(**item)
    assert report.game_version == RETAIL.wcl_game_version


def test_overview_loader_sets_game_version_from_master_data() -> None:
    report = UserReport(report_id="abc")
    loader = ReportOverviewLoader(report, game_data_with())
    loader.process_query_result({"report": {"masterData": {"actors": [], "gameVersion": 5}}})
    assert report.game_version == 5


def test_overview_loader_without_game_version_keeps_retail() -> None:
    report = UserReport(report_id="abc")
    loader = ReportOverviewLoader(report)
    loader.process_query_result({"report": {"masterData": {"actors": []}}})
    assert report.game_version == RETAIL.wcl_game_version


def test_overview_query_asks_for_game_version() -> None:
    assert "gameVersion" in ReportOverviewLoader(UserReport(report_id="abc")).get_query()


def test_loaded_user_report_stores_game_version() -> None:
    report = UserReport(report_id="abc")
    ReportOverviewLoader(report, game_data_with()).process_query_result(
        {"report": {"masterData": {"actors": [], "gameVersion": 5}}},
    )

    with mock.patch.object(DynamoDBModel, "get_table") as get_table:
        report.save()

    item = get_table.return_value.put_item.call_args.kwargs["Item"]
    assert item["game_version"] == 5


################################################################################
# UserReport: the Game Version comes from the log
#


def test_overview_loader_picks_the_game_data_from_the_log() -> None:
    report = UserReport(report_id="abc")
    loader = ReportOverviewLoader(report)
    loader.process_query_result({"report": {"masterData": {"actors": [], "gameVersion": MISTS.wcl_game_version}}})
    assert loader.game_data is MISTS.data


def test_overview_loader_without_game_version_in_the_log_uses_retail() -> None:
    loader = ReportOverviewLoader(UserReport(report_id="abc"))
    loader.process_query_result({"report": {"masterData": {"actors": []}}})
    assert loader.game_data is RETAIL.data


def test_overview_loader_rejects_an_unsupported_game_version_naming_it() -> None:
    loader = ReportOverviewLoader(UserReport(report_id="abc"))
    with pytest.raises(UnsupportedGameVersionError, match="5"):
        loader.process_query_result({"report": {"masterData": {"actors": [], "gameVersion": 5}}})


################################################################################
# Comp rankings
#


def test_comp_ranking_load_rejects_another_game_version() -> None:
    import asyncio

    ranking = CompRanking(game_version="mists", boss_slug="b")
    with pytest.raises(ValueError, match="belongs to Game Version 'mists', not 'retail'"):
        asyncio.run(ranking.load(RETAIL))
