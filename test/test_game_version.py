"""Seams: the `LORRGS_GAME_VERSION` env var picks the active Game Version at import time.

Each case runs in a fresh interpreter, because the Game Version is resolved once at import.
"""

from __future__ import annotations

import os
import subprocess
import sys

import pytest

from lorgs import game_version


def _run(code: str, env_value: str | None) -> subprocess.CompletedProcess[str]:
    env = {k: v for k, v in os.environ.items() if k != "LORRGS_GAME_VERSION"}
    if env_value is not None:
        env["LORRGS_GAME_VERSION"] = env_value
    env["PYTHONPATH"] = "."
    return subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, check=False)


@pytest.mark.parametrize(
    ("env_value", "expected"),
    [
        (None, "retail"),
        ("", "retail"),  # a blank line in `.env` means "use the default"
        ("retail", "retail"),
        ("forever", "forever"),
        ("mists", "mists"),
    ],
)
def test_active_game_version_follows_env(env_value: str | None, expected: str) -> None:
    result = _run("from lorgs.game_version import ACTIVE; print(ACTIVE.name)", env_value)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == expected


@pytest.mark.parametrize("env_value", ["classic", "retail2", "wow"])
def test_unknown_game_version_fails_at_import(env_value: str) -> None:
    result = _run("import lorgs.game_version", env_value)
    assert result.returncode != 0
    assert "KeyError" in result.stderr


@pytest.mark.parametrize("env_value", [None, "forever", "mists"])
def test_importing_game_version_does_not_import_game_data(env_value: str | None) -> None:
    code = "import sys; import lorgs.game_version; print(sorted(m for m in sys.modules if m.startswith('lorgs.data')))"
    result = _run(code, env_value)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "[]"


def test_game_version_config() -> None:
    from lorgs.game_version import MISTS, FOREVER, RETAIL
    from lorgs.models.difficulty import RaidDifficulty

    assert RETAIL.s3_prefix == ""
    assert RETAIL.difficulties == (RaidDifficulty.HEROIC, RaidDifficulty.MYTHIC)
    assert RETAIL.default_difficulty is RaidDifficulty.MYTHIC
    assert RETAIL.wcl_game_version == 1
    assert RETAIL.data_package == "lorgs.data.retail"

    assert FOREVER.s3_prefix == "forever/"
    assert FOREVER.difficulties == (RaidDifficulty.NORMAL,)
    assert FOREVER.default_difficulty is RaidDifficulty.NORMAL
    assert FOREVER.data_package == "lorgs.data.forever"

    assert MISTS.s3_prefix == "mists/"
    assert MISTS.difficulties == (RaidDifficulty.NORMAL, RaidDifficulty.HEROIC)
    assert MISTS.default_difficulty is RaidDifficulty.HEROIC
    assert MISTS.wcl_game_version == 6
    assert MISTS.data_package == "lorgs.data.mists"


################################################################################
# Difficulties come from the active Game Version
#


def test_difficulty_names() -> None:
    from lorgs.game_version import MISTS, FOREVER, RETAIL

    assert RETAIL.difficulty_names == ("heroic", "mythic")
    assert RETAIL.default_difficulty_name == "mythic"
    assert FOREVER.difficulty_names == ("normal",)
    assert FOREVER.default_difficulty_name == "normal"
    assert MISTS.difficulty_names == ("normal", "heroic")
    assert MISTS.default_difficulty_name == "heroic"


@pytest.mark.parametrize(
    ("env_value", "expected"),
    [(None, "mythic"), ("forever", "normal"), ("mists", "heroic")],
)
def test_default_difficulty_follows_active_game_version(env_value: str | None, expected: str) -> None:
    code = (
        "from lorgs.models.task_payloads import SpecRankingPayload\n"
        "from lorgs.models.warcraftlogs_ranking import SpecRanking\n"
        "from lorrgs_api.routes import api_spec_rankings\n"
        "import inspect\n"
        "route_defaults = {\n"
        "    inspect.signature(f).parameters['difficulty'].default\n"
        "    for f in (api_spec_rankings.get_spec_ranking, api_spec_rankings.get_spec_ranking_info, api_spec_rankings.flag_dirty)\n"
        "}\n"
        "print(SpecRankingPayload(boss_slug='b', spec_slug='s').difficulty, SpecRanking(spec_slug='s', boss_slug='b').difficulty, *route_defaults)\n"
    )
    result = _run(code, env_value)
    assert result.returncode == 0, result.stderr
    assert result.stdout.split() == [expected] * 3


@pytest.mark.parametrize(
    ("env_value", "expected"),
    [(None, ["heroic", "mythic"]), ("forever", ["normal"]), ("mists", ["normal", "heroic"])],
)
def test_difficulty_all_expands_to_the_game_version_difficulties(env_value: str | None, expected: list[str]) -> None:
    code = (
        "from lorrgs_sqs.helpers import expand_payload\n"
        "print([p['difficulty'] for p in expand_payload('difficulty', {'difficulty': 'all'})])\n"
    )
    result = _run(code, env_value)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == str(expected)


################################################################################
# Data test directories only run under their own Game Version
#


@pytest.mark.parametrize(
    ("directory", "wrong_env_value", "right_env_value"),
    [
        ("test/data_retail", "forever", None),
        ("test/data_retail", "mists", None),
        ("test/data_forever", None, "forever"),
        ("test/data_forever", "retail", "forever"),
        ("test/data_forever", "mists", "forever"),
        ("test/data_mists", None, "mists"),
    ],
)
def test_data_directories_fail_under_the_wrong_game_version(
    directory: str,
    wrong_env_value: str | None,
    right_env_value: str | None,
) -> None:
    def pytest_in(env_value: str | None) -> subprocess.CompletedProcess[str]:
        code = f"import sys, pytest; sys.exit(pytest.main(['-q', '-p', 'no:cacheprovider', '{directory}']))"
        return _run(code, env_value)

    wrong = pytest_in(wrong_env_value)
    assert wrong.returncode != 0
    assert "LORRGS_GAME_VERSION" in wrong.stdout + wrong.stderr
    assert "passed" not in wrong.stdout

    right = pytest_in(right_env_value)
    assert right.returncode == 0, right.stdout + right.stderr


################################################################################
# API: list of Game Versions
#


def test_game_versions_route_lists_all_game_versions(monkeypatch: pytest.MonkeyPatch) -> None:
    from lorgs import game_version
    from test.helpers import get_api_routes

    monkeypatch.setenv("LORRGS_API_URL_MISTS", "http://127.0.0.1:5014/")
    status, body = get_api_routes("/api/game_versions")["/api/game_versions"]

    assert status == 200
    assert [version["name"] for version in body] == ["retail", "mists", "forever"]
    assert [version["name"] for version in body if version["active"]] == [game_version.ACTIVE.name]

    by_name = {version["name"]: version for version in body}
    assert by_name["retail"]["collapse_raids"] is False
    assert by_name["retail"]["has_comp_modes"] is True
    assert by_name["mists"]["collapse_raids"] is True
    assert by_name["mists"]["has_comp_modes"] is False
    assert by_name["mists"]["api_url"] == "http://127.0.0.1:5014"  # trailing slash stripped
    assert by_name["forever"]["api_url"] == ""  # not configured
