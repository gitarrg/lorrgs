"""Seams: the active Game Version picks which data package `lorgs.data` loads.

Each case runs in a fresh interpreter, because the Game Version is resolved once at import.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import textwrap

import pytest


def _run(code: str, env_value: str | None) -> subprocess.CompletedProcess[str]:
    env = {k: v for k, v in os.environ.items() if k != "LORRGS_GAME_VERSION"}
    if env_value is not None:
        env["LORRGS_GAME_VERSION"] = env_value
    env["PYTHONPATH"] = "."
    env.setdefault("SECRET_KEY", "test-secret")  # the API refuses to start without one
    return subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, check=False)


# Starts the API app and GETs routes through its ASGI interface (no server, no network, no httpx).
GET_ROUTES = textwrap.dedent(
    """
    import asyncio, json, sys

    from lorrgs_api.app import create_app

    ROUTES = sys.argv[1:] or ["/api/roles", "/api/classes", "/api/specs", "/api/zones", "/api/bosses",
                              "/api/spells", "/api/trinkets", "/api/seasons/current"]

    async def get(app, path):
        body = b""
        status = 0

        async def receive():
            return {"type": "http.request", "body": b"", "more_body": False}

        async def send(message):
            nonlocal body, status
            if message["type"] == "http.response.start":
                status = message["status"]
            elif message["type"] == "http.response.body":
                body += message.get("body", b"")

        scope = {"type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1", "method": "GET",
                 "scheme": "https", "path": path, "raw_path": path.encode(), "query_string": b"",
                 "headers": [], "client": ("127.0.0.1", 1), "server": ("test", 443)}
        await app(scope, receive, send)
        return status, json.loads(body)

    async def main():
        app = create_app()
        print(json.dumps({route: await get(app, route) for route in ROUTES}))

    asyncio.run(main())
    """
)


def _get_routes(env_value: str | None) -> dict[str, tuple[int, object]]:
    result = _run(GET_ROUTES, env_value)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout.strip().splitlines()[-1])


def test_forever_api_starts_and_world_data_is_empty() -> None:
    routes = _get_routes("forever")

    assert {route: status for route, (status, _) in routes.items()} == dict.fromkeys(routes, 200)
    assert routes["/api/classes"][1] == {}
    assert routes["/api/specs"][1] == {"specs": []}
    assert routes["/api/zones"][1] == []
    assert routes["/api/bosses"][1] == {"bosses": []}
    assert routes["/api/spells"][1] == {}
    assert routes["/api/trinkets"][1] == {}
    assert routes["/api/seasons/current"][1]["raids"] == []
    assert routes["/api/roles"][1]["roles"], "roles are shared between Game Versions"


def test_retail_api_serves_world_data() -> None:
    routes = _get_routes(None)

    assert routes["/api/specs"][1]["specs"]
    assert routes["/api/zones"][1]
    assert routes["/api/bosses"][1]["bosses"]
    assert routes["/api/seasons/current"][1]["raids"]


@pytest.mark.parametrize(
    ("env_value", "loaded", "not_loaded"),
    [
        (None, "lorgs.data.retail", "lorgs.data.forever"),
        ("forever", "lorgs.data.forever", "lorgs.data.retail"),
    ],
)
def test_only_the_active_game_versions_package_is_loaded(env_value: str | None, loaded: str, not_loaded: str) -> None:
    code = (
        "import sys, lorgs.data\n"
        "print(sorted(m for m in sys.modules if m.startswith('lorgs.data.')\n"
        "             and m.split('.')[2] in {'retail', 'forever', 'expansions'}))"
    )
    result = _run(code, env_value)
    assert result.returncode == 0, result.stderr
    modules = result.stdout.strip()
    assert loaded in modules
    assert not_loaded not in modules
    if env_value == "forever":
        assert "expansions" not in modules, "Forever imports no expansions yet"


def test_current_season_is_exported_by_the_active_package() -> None:
    code = "from lorgs.data import CURRENT_SEASON; print(CURRENT_SEASON.slug)"
    assert _run(code, None).stdout.strip() == "midnight_s2"
    assert _run(code, "forever").stdout.strip() == "forever"


def test_forever_task_keywords_expand_to_nothing() -> None:
    code = (
        "from lorrgs_sqs.helpers import PAYLOAD_EXPANDERS as P\n"
        "print(len(P['spec_slug']), len(P['boss_slug']))"
    )
    assert _run(code, "forever").stdout.strip() == "0 0"
    retail_specs, retail_bosses = map(int, _run(code, None).stdout.split())
    assert retail_specs > 0
    assert retail_bosses > 0
