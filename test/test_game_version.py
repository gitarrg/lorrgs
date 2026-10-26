"""Seams: the `LORRGS_GAME_VERSION` env var picks the active Game Version at import time.

Each case runs in a fresh interpreter, because the Game Version is resolved once at import.
"""

from __future__ import annotations

import os
import subprocess
import sys

import pytest


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
        ("Forever", "forever"),
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
    assert "LORRGS_GAME_VERSION" in result.stderr


@pytest.mark.parametrize("env_value", [None, "forever"])
def test_importing_game_version_does_not_import_game_data(env_value: str | None) -> None:
    code = "import sys; import lorgs.game_version; print(sorted(m for m in sys.modules if m.startswith('lorgs.data')))"
    result = _run(code, env_value)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "[]"


def test_retail_and_forever_config() -> None:
    from lorgs.game_version import FOREVER, RETAIL
    from lorgs.models.difficulty import RaidDifficulty

    assert RETAIL.s3_prefix == ""
    assert RETAIL.difficulties == (RaidDifficulty.HEROIC, RaidDifficulty.MYTHIC)
    assert RETAIL.default_difficulty is RaidDifficulty.MYTHIC
    assert RETAIL.wcl_game_versions == frozenset({1})
    assert RETAIL.data_package == "lorgs.data.retail"

    assert FOREVER.s3_prefix == "forever/"
    assert FOREVER.difficulties == (RaidDifficulty.NORMAL,)
    assert FOREVER.default_difficulty is RaidDifficulty.NORMAL
    assert FOREVER.data_package == "lorgs.data.forever"
