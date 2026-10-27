"""Seams: with Forever active, the API starts with Forever's world data: classes and specs, but no spells or raids yet."""

from lorrgs_sqs.helpers import PAYLOAD_EXPANDERS
from test.helpers import get_api_routes


WORLD_DATA_ROUTES = ["/api/roles", "/api/classes", "/api/specs", "/api/zones", "/api/bosses", "/api/spells", "/api/trinkets", "/api/seasons/current"]


def test_api_starts_and_serves_classes_and_specs() -> None:
    routes = get_api_routes(*WORLD_DATA_ROUTES)

    assert {route: status for route, (status, _) in routes.items()} == dict.fromkeys(routes, 200)
    assert len(routes["/api/classes"][1]) == 9
    assert len(routes["/api/specs"][1]["specs"]) == 27
    assert routes["/api/zones"][1] == []
    assert routes["/api/bosses"][1] == {"bosses": []}
    assert routes["/api/spells"][1] == {}
    assert routes["/api/trinkets"][1] == {}
    assert routes["/api/seasons/current"][1]["raids"] == []
    assert routes["/api/roles"][1]["roles"], "roles are shared between Game Versions"


def test_current_season_is_the_placeholder() -> None:
    from lorgs.data import CURRENT_SEASON

    assert CURRENT_SEASON.slug == "forever"


def test_task_keywords_expand_to_the_specs() -> None:
    assert len(PAYLOAD_EXPANDERS["spec_slug"]) == 27
    assert PAYLOAD_EXPANDERS["boss_slug"] == []  # no raids yet
    assert PAYLOAD_EXPANDERS["difficulty"]({}) == ["normal"]
