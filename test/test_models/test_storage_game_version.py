"""Seams: storage goes through the active Game Version.

- S3 keys are prefixed with `GameVersion.s3_prefix` (empty for Retail).
- DynamoDB keys are shared between Game Versions (ADR 0002).
- A User Report records the WCL game version of its log; items without it are Retail.
"""

from __future__ import annotations

import io
import os
import subprocess
import sys
from unittest import mock

import pytest

from lorgs import game_version
from lorgs.loaders.report_overview_loader import ReportOverviewLoader
from lorgs.models.base.dynamodb import DynamoDBModel
from lorgs.models.user import User
from lorgs.models.warcraftlogs_comp_ranking import CompRanking
from lorgs.models.warcraftlogs_ranking import SpecRanking
from lorgs.models.warcraftlogs_user_report import UserReport


SPEC_RANKING_KWARGS = {"spec_slug": "mage-fire", "boss_slug": "some-boss", "difficulty": "mythic", "metric": "dps"}


@pytest.fixture
def active_retail(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(game_version, "ACTIVE", game_version.RETAIL)


@pytest.fixture
def active_forever(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(game_version, "ACTIVE", game_version.FOREVER)


################################################################################
# S3 keys
#


@pytest.mark.usefixtures("active_retail")
def test_retail_s3_keys_are_unprefixed() -> None:
    assert SpecRanking.get_key(**SPEC_RANKING_KWARGS) == "spec_ranking/mage-fire/some-boss__mythic__dps"
    assert CompRanking.get_key(boss_slug="some-boss") == "comp_ranking/some-boss"


@pytest.mark.usefixtures("active_forever")
def test_forever_s3_keys_are_prefixed() -> None:
    assert SpecRanking.get_key(**SPEC_RANKING_KWARGS) == "forever/spec_ranking/mage-fire/some-boss__mythic__dps"
    assert CompRanking.get_key(boss_slug="some-boss") == "forever/comp_ranking/some-boss"


@pytest.mark.usefixtures("active_forever")
def test_save_and_get_use_the_prefixed_key() -> None:
    ranking = SpecRanking(**SPEC_RANKING_KWARGS)
    expected_key = "forever/spec_ranking/mage-fire/some-boss__mythic__dps"

    with mock.patch("lorgs.models.base.s3.s3client") as s3client:
        ranking.save()
        assert s3client.put_object.call_args.kwargs["Key"] == expected_key

        s3client.get_object.return_value = {"Body": io.BytesIO(ranking.model_dump_json().encode())}
        SpecRanking.get(**SPEC_RANKING_KWARGS)
        assert s3client.get_object.call_args.kwargs["Key"] == expected_key


def test_env_var_picks_the_s3_prefix() -> None:
    code = "from lorgs.models.warcraftlogs_comp_ranking import CompRanking; print(CompRanking.get_key(boss_slug='b'))"
    env = {k: v for k, v in os.environ.items() if k != "LORRGS_GAME_VERSION"}
    env.update(PYTHONPATH=".", LORRGS_GAME_VERSION="forever")
    result = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "forever/comp_ranking/b"


################################################################################
# DynamoDB keys stay shared
#


@pytest.mark.usefixtures("active_forever")
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
    assert report.game_version in game_version.RETAIL.wcl_game_versions


def test_overview_loader_sets_game_version_from_master_data() -> None:
    report = UserReport(report_id="abc")
    loader = ReportOverviewLoader(report)
    loader.process_query_result({"report": {"masterData": {"actors": [], "gameVersion": 5}}})
    assert report.game_version == 5


def test_overview_loader_without_game_version_keeps_retail() -> None:
    report = UserReport(report_id="abc")
    loader = ReportOverviewLoader(report)
    loader.process_query_result({"report": {"masterData": {"actors": []}}})
    assert report.game_version in game_version.RETAIL.wcl_game_versions


def test_overview_query_asks_for_game_version() -> None:
    assert "gameVersion" in ReportOverviewLoader(UserReport(report_id="abc")).get_query()


def test_loaded_user_report_stores_game_version() -> None:
    report = UserReport(report_id="abc")
    ReportOverviewLoader(report).process_query_result({"report": {"masterData": {"actors": [], "gameVersion": 5}}})

    with mock.patch.object(DynamoDBModel, "get_table") as get_table:
        report.save()

    item = get_table.return_value.put_item.call_args.kwargs["Item"]
    assert item["game_version"] == 5
