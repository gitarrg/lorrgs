"""Seams: the API serves Retail's world data and task keywords expand to it."""

from lorrgs_sqs.helpers import PAYLOAD_EXPANDERS
from test.helpers import get_api_routes


WORLD_DATA_ROUTES = [
    "/api/retail/roles",
    "/api/retail/classes",
    "/api/retail/specs",
    "/api/retail/zones",
    "/api/retail/bosses",
    "/api/retail/spells",
    "/api/retail/trinkets",
    "/api/retail/seasons/current",
]


def test_api_serves_world_data() -> None:
    routes = get_api_routes(*WORLD_DATA_ROUTES)

    assert {route: status for route, (status, _) in routes.items()} == dict.fromkeys(routes, 200)
    assert routes["/api/retail/specs"][1]["specs"]
    assert routes["/api/retail/zones"][1]
    assert routes["/api/retail/bosses"][1]["bosses"]
    assert routes["/api/retail/seasons/current"][1]["raids"]


def test_current_season_is_midnight_season_2() -> None:
    from lorgs.data.retail import GAME_DATA

    assert GAME_DATA.season.slug == "midnight_s2"


def test_task_keywords_expand_to_specs_and_bosses() -> None:
    assert PAYLOAD_EXPANDERS["spec_slug"]({"game_version": "retail"})
    assert PAYLOAD_EXPANDERS["boss_slug"]({"game_version": "retail"})
    assert PAYLOAD_EXPANDERS["difficulty"]({"game_version": "retail"}) == ["heroic", "mythic"]


def test_only_the_current_season_is_served() -> None:
    routes = get_api_routes("/api/retail/seasons/midnight_s2", "/api/retail/seasons/midnight_s1")

    assert routes["/api/retail/seasons/midnight_s2"][0] == 200
    assert routes["/api/retail/seasons/midnight_s1"][0] == 404
