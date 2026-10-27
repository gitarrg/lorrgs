"""Seams: with Retail active, the API serves Retail's world data and task keywords expand to it."""

from lorrgs_sqs.helpers import PAYLOAD_EXPANDERS
from test.helpers import get_api_routes


WORLD_DATA_ROUTES = ["/api/roles", "/api/classes", "/api/specs", "/api/zones", "/api/bosses", "/api/spells", "/api/trinkets", "/api/seasons/current"]


def test_api_serves_world_data() -> None:
    routes = get_api_routes(*WORLD_DATA_ROUTES)

    assert {route: status for route, (status, _) in routes.items()} == dict.fromkeys(routes, 200)
    assert routes["/api/specs"][1]["specs"]
    assert routes["/api/zones"][1]
    assert routes["/api/bosses"][1]["bosses"]
    assert routes["/api/seasons/current"][1]["raids"]


def test_current_season_is_midnight_season_2() -> None:
    from lorgs.data import CURRENT_SEASON

    assert CURRENT_SEASON.slug == "midnight_s2"


def test_task_keywords_expand_to_specs_and_bosses() -> None:
    assert PAYLOAD_EXPANDERS["spec_slug"]
    assert PAYLOAD_EXPANDERS["boss_slug"]
    assert PAYLOAD_EXPANDERS["difficulty"]({}) == ["heroic", "mythic"]
