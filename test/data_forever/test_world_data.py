"""Seams: the API starts with Forever's world data: classes and specs, but no spells or raids yet."""

from lorrgs_sqs.helpers import PAYLOAD_EXPANDERS
from test.helpers import get_api_routes


WORLD_DATA_ROUTES = ["/api/forever/roles", "/api/forever/classes", "/api/forever/specs", "/api/forever/zones", "/api/forever/bosses", "/api/forever/spells", "/api/forever/trinkets", "/api/forever/seasons/current"]


def test_api_starts_and_serves_classes_and_specs() -> None:
    routes = get_api_routes(*WORLD_DATA_ROUTES)

    assert {route: status for route, (status, _) in routes.items()} == dict.fromkeys(routes, 200)
    assert len(routes["/api/forever/classes"][1]) == 9
    assert len(routes["/api/forever/specs"][1]["specs"]) == 27
    assert routes["/api/forever/zones"][1] == []
    assert routes["/api/forever/bosses"][1] == {"bosses": []}
    assert routes["/api/forever/spells"][1] == {}
    assert routes["/api/forever/trinkets"][1] == {}
    assert routes["/api/forever/seasons/current"][1]["raids"] == []
    assert routes["/api/forever/roles"][1]["roles"], "every Game Version has its own roles"


def test_current_season_is_the_placeholder() -> None:
    from lorgs.data.forever import CURRENT_SEASON

    assert CURRENT_SEASON.slug == "forever"


def test_task_keywords_expand_to_the_specs() -> None:
    assert len(PAYLOAD_EXPANDERS["spec_slug"]({"game_version": "forever"})) == 27
    assert PAYLOAD_EXPANDERS["boss_slug"]({"game_version": "forever"}) == []  # no raids yet
    assert PAYLOAD_EXPANDERS["difficulty"]({"game_version": "forever"}) == ["normal"]
