"""Seams: the active Game Version picks which data package `lorgs.data` loads.

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
    env.setdefault("SECRET_KEY", "test-secret")  # the API refuses to start without one
    return subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, check=False)


@pytest.mark.parametrize(
    ("env_value", "loaded", "not_loaded"),
    [
        (None, "lorgs.data.retail", "lorgs.data.forever"),
        ("forever", "lorgs.data.forever", "lorgs.data.retail"),
        ("classic_mop", "lorgs.data.classic_mop", "lorgs.data.retail"),
    ],
)
def test_only_the_active_game_versions_package_is_loaded(env_value: str | None, loaded: str, not_loaded: str) -> None:
    code = (
        "import sys, lorgs.data\n"
        "print(sorted(m for m in sys.modules if m.startswith('lorgs.data.')\n"
        "             and m.split('.')[2] in {'retail', 'forever', 'classic_mop', 'expansions'}))"
    )
    result = _run(code, env_value)
    assert result.returncode == 0, result.stderr
    modules = result.stdout.strip()
    assert loaded in modules
    assert not_loaded not in modules
    if env_value == "forever":
        assert "expansions" not in modules, "Forever imports no expansions yet"
