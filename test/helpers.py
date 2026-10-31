import asyncio
import os
import json
import typing


ROOT = "./test/fixtures/"


def game_data_with(*, bosses: typing.Sequence = (), specs: typing.Sequence = ()):
    """Game Data holding just these bosses and specs."""
    from lorgs.models.difficulty import RaidDifficulty
    from lorgs.models.game_data import GameData
    from lorgs.models.raid_zone import RaidZone
    from lorgs.models.season import Season

    season = Season(name="Test Season", ilvl=1, raids=[RaidZone(id=990000, name="Test Raid", bosses=list(bosses))])
    classes = list({spec.wow_class for spec in specs})
    roles = list({spec.role for spec in specs})
    return GameData(roles=roles, classes=classes, season=season, difficulties=(RaidDifficulty.HEROIC,))


def save_fixture(filename: str, content):

    file_path = os.path.join(ROOT, filename)
    with open(file_path, "w", encoding="utf-8") as json_file:
        return json.dump(
            content,
            json_file,
            indent=4,
        )


def load_fixture(filename: str):

    file_path = os.path.join(ROOT, filename)
    with open(file_path, "rb") as json_file:
        return json.load(json_file)


def report_query(**report: typing.Any):
    """A report query result as `WarcraftlogsClient.query` returns it, parsed the way loaders get it."""
    from lorgs.clients import wcl

    return wcl.Query.model_validate({"reportData": {"report": report}})


def events_query(events: typing.Iterable[dict[str, typing.Any]]):
    """A report query result holding just these events."""
    return report_query(events={"data": list(events)})


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
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": "GET",
            "scheme": "https",
            "path": path,
            "raw_path": path.encode(),
            "query_string": b"",
            "headers": [],
            "client": ("127.0.0.1", 1),
            "server": ("test", 443),
        }
        await app(scope, receive, send)
        return status, json.loads(body)

    async def main() -> dict[str, tuple[int, typing.Any]]:
        app = create_app()
        return {path: await get(app, path) for path in paths}

    return asyncio.run(main())


def game_version_with(game_data, name: str = "retail"):
    """A Game Version around the given Game Data."""
    from lorgs.models.game_version import GameVersion

    return GameVersion(name=name, title=name, wcl_game_version=1, data=game_data)
