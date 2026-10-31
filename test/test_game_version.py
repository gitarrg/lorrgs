"""Seams: the static configuration of the Game Versions, and the API route that lists them."""

from __future__ import annotations

from lorgs.data import FOREVER, GAME_VERSIONS, MISTS, RETAIL, get_game_version_by_wcl_id
from lorgs.models.difficulty import RaidDifficulty
from test.helpers import get_api_routes


def test_game_version_config() -> None:
    assert RETAIL.s3_prefix == "retail/"
    assert RETAIL.difficulties == (RaidDifficulty.HEROIC, RaidDifficulty.MYTHIC)
    assert RETAIL.default_difficulty is RaidDifficulty.MYTHIC
    assert RETAIL.wcl_game_version == 1

    assert FOREVER.s3_prefix == "forever/"
    assert FOREVER.difficulties == (RaidDifficulty.NORMAL,)
    assert FOREVER.default_difficulty is RaidDifficulty.NORMAL

    assert MISTS.s3_prefix == "mists/"
    assert MISTS.difficulties == (RaidDifficulty.HEROIC,)
    assert MISTS.default_difficulty is RaidDifficulty.HEROIC
    assert MISTS.wcl_game_version == 6


def test_difficulty_names() -> None:
    assert RETAIL.difficulty_names == ("heroic", "mythic")
    assert RETAIL.default_difficulty_name == "mythic"
    assert FOREVER.difficulty_names == ("normal",)
    assert FOREVER.default_difficulty_name == "normal"
    assert MISTS.difficulty_names == ("heroic",)
    assert MISTS.default_difficulty_name == "heroic"


def test_game_version_by_wcl_id() -> None:
    assert get_game_version_by_wcl_id(1) is RETAIL
    assert get_game_version_by_wcl_id(6) is MISTS
    assert get_game_version_by_wcl_id(12345) is None


def test_game_versions_route_lists_all_game_versions() -> None:
    status, body = get_api_routes("/api/game_versions")["/api/game_versions"]

    assert status == 200
    assert [version["name"] for version in body] == list(GAME_VERSIONS)
    assert all("active" not in version and "api_url" not in version for version in body)

    by_name = {version["name"]: version for version in body}
    assert by_name["retail"]["collapse_raids"] is False
    assert by_name["retail"]["has_comp_modes"] is True
    assert by_name["retail"]["has_talents"] is True
    assert by_name["mists"]["has_talents"] is False
    assert by_name["retail"]["wcl_game_version"] == 1
    assert by_name["mists"]["collapse_raids"] is True
    assert by_name["mists"]["has_comp_modes"] is False
