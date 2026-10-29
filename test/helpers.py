

import asyncio
import os
import json
import typing

import pytest


ROOT = "./test/fixtures/"


def game_data_with(*, bosses: typing.Sequence = (), specs: typing.Sequence = ()):
    """Game Data holding just these bosses and specs."""
    from lorgs.models.game_data import GameData
    from lorgs.models.raid_zone import RaidZone
    from lorgs.models.season import Season

    season = Season(name="Test Season", ilvl=1, raids=[RaidZone(id=990000, name="Test Raid", bosses=list(bosses))])
    classes = list({spec.wow_class for spec in specs})
    roles = list({spec.role for spec in specs})
    return GameData(roles=roles, classes=classes, seasons=[season], current_season=season)


def save_fixture(filename: str, content):

    file_path = os.path.join(ROOT, filename)
    with open(file_path, "w", encoding="utf-8") as json_file:
        return json.dump(
            content, json_file,
            indent=4,
        )


def load_fixture(filename: str):

    file_path = os.path.join(ROOT, filename)
    with open(file_path, "rb") as json_file:
        return json.load(json_file)


def wrap_data(data: typing.Any, *parents: str):
    """Wraps the `data` in a nested dict.
    
    Example:
        >>> wrap_data([1, 2, 3], "foo", "bar")
        {'foo': {'bar': [1, 2, 3]}}
    """
    parents = parents[::-1]
    for parent in parents:
        data = {parent: data}
    return data


def require_game_version(name: str) -> None:
    """Abort the run unless the active Game Version is `name`.

    Called by the `conftest.py` of each `test/data_<game version>/` directory: those tests use
    the real game data, which is only loaded for the active Game Version.
    """
    from lorgs import game_version

    if game_version.ACTIVE.name != name:
        msg = (
            f"test/data_{name} needs LORRGS_GAME_VERSION={name}, "
            f"but the active Game Version is {game_version.ACTIVE.name!r}."
        )
        raise pytest.UsageError(msg)


def get_api_routes(*paths: str) -> dict[str, tuple[int, typing.Any]]:
    """GET routes of the API app through its ASGI interface (no server, no network).

    Returns `{path: (status, json body)}`.
    """
    os.environ.setdefault("SECRET_KEY", "test-secret")  # the API refuses to start without one
    from lorrgs_api.app import create_app

    async def get(app: typing.Any, path: str) -> tuple[int, typing.Any]:
        body = b""
        status = 0

        async def receive() -> dict[str, typing.Any]:
            return {"type": "http.request", "body": b"", "more_body": False}

        async def send(message: dict[str, typing.Any]) -> None:
            nonlocal body, status
            if message["type"] == "http.response.start":
                status = message["status"]
            elif message["type"] == "http.response.body":
                body += message.get("body", b"")

        scope = {
            "type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1", "method": "GET",
            "scheme": "https", "path": path, "raw_path": path.encode(), "query_string": b"",
            "headers": [], "client": ("127.0.0.1", 1), "server": ("test", 443),
        }
        await app(scope, receive, send)
        return status, json.loads(body)

    async def main() -> dict[str, tuple[int, typing.Any]]:
        app = create_app()
        return {path: await get(app, path) for path in paths}

    return asyncio.run(main())


def assert_game_data_matches_registry() -> None:
    """The active Game Version's `GameData` holds objects of the `MemoryModel` registry.

    Runs in a fresh interpreter: other tests register their own objects in the (process wide) registry.
    """
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "-c", "from test.helpers import _assert_game_data_matches_registry as f; f()"],
        capture_output=True, text=True, check=False, env={**os.environ, "PYTHONPATH": "."},
    )
    assert result.returncode == 0, result.stdout + result.stderr


def _assert_game_data_matches_registry() -> None:
    """The active Game Version's `GameData` holds objects of the `MemoryModel` registry."""
    from lorgs.data import GAME_DATA
    from lorgs.models.dungeon import Dungeon
    from lorgs.models.raid_boss import RaidBoss
    from lorgs.models.raid_zone import RaidZone
    from lorgs.models.season import Season
    from lorgs.models.wow_class import WowClass
    from lorgs.models.wow_role import WowRole
    from lorgs.models.wow_spec import WowSpec
    from lorgs.models.wow_spell import WowSpell

    exact = [
        (WowRole, GAME_DATA.roles),
        (WowClass, GAME_DATA.classes),
        (WowSpec, GAME_DATA.specs),
        (Season, GAME_DATA.seasons),
    ]
    for model, objects in exact:
        assert {id(obj) for obj in objects} == {id(obj) for obj in model.list()}, model.__name__

    # only the current season's raids and dungeons are Game Data: the registry holds older ones too
    subsets = [
        (RaidZone, GAME_DATA.zones),
        (RaidBoss, GAME_DATA.bosses),
        (Dungeon, GAME_DATA.dungeons),
    ]
    for model, objects in subsets:
        assert {id(obj) for obj in objects} <= {id(obj) for obj in model.list()}, model.__name__
    assert GAME_DATA.zones == GAME_DATA.current_season.raids
    assert GAME_DATA.dungeons == GAME_DATA.current_season.dungeons

    # `add_buff(spell)` stores a copy, which an Actor Type holds but the registry never saw
    registered = {id(spell) for spell in WowSpell.list()}
    held = {id(spell) for spell in GAME_DATA.spells}
    buff_copies = {
        id(buff) for actor in [*GAME_DATA.classes, *GAME_DATA.specs, *GAME_DATA.bosses] for buff in actor.buffs
    }
    assert held - registered <= buff_copies
