"""Seams: the API starts with Forever's world data: classes, specs and the Classic raids and the first class spells."""

from lorrgs_sqs.helpers import PAYLOAD_EXPANDERS
from test.helpers import get_api_routes


WORLD_DATA_ROUTES = [
    "/api/forever/roles",
    "/api/forever/classes",
    "/api/forever/specs",
    "/api/forever/zones",
    "/api/forever/bosses",
    "/api/forever/spells",
    "/api/forever/trinkets",
    "/api/forever/seasons/current",
]


def test_api_starts_and_serves_classes_and_specs() -> None:
    routes = get_api_routes(*WORLD_DATA_ROUTES)

    assert {route: status for route, (status, _) in routes.items()} == dict.fromkeys(routes, 200)
    assert len(routes["/api/forever/classes"][1]) == 9
    assert len(routes["/api/forever/specs"][1]["specs"]) == 27
    assert len(routes["/api/forever/zones"][1]) == 1
    assert len(routes["/api/forever/bosses"][1]["bosses"]) == 1
    assert "2687" in routes["/api/forever/spells"][1], "Bloodrage"
    assert routes["/api/forever/trinkets"][1] == {}
    assert len(routes["/api/forever/seasons/current"][1]["raids"]) == 1
    assert routes["/api/forever/roles"][1]["roles"], "every Game Version has its own roles"


def test_current_season_is_forever() -> None:
    from lorgs.data.forever import GAME_DATA

    assert GAME_DATA.season.slug == "forever"


def test_task_keywords_expand_to_the_specs() -> None:
    assert len(PAYLOAD_EXPANDERS["spec_slug"]({"game_version": "forever"})) == 27
    assert len(PAYLOAD_EXPANDERS["boss_slug"]({"game_version": "forever"})) == 1
    assert PAYLOAD_EXPANDERS["difficulty"]({"game_version": "forever"}) == ["normal"]


def test_onyxia_has_the_warcraft_logs_forever_ids() -> None:
    """Zone 3001 and encounter 251084, as Warcraft Logs reports them for the Forever logs (gameVersion 7)."""
    from lorgs.data.forever import GAME_DATA

    onyxia = GAME_DATA.get_boss(boss_id=251084)
    assert onyxia is not None
    assert onyxia.zone.id == 3001
