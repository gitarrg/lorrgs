"""Forever's dungeons are served for User Reports (never ranked)."""

from __future__ import annotations

from test.helpers import get_api_routes

from lorgs.models.dungeon import FALLBACK_ICON


def test_dungeons_are_listed_with_the_fallback_icon() -> None:
    status, body = get_api_routes("/api/forever/dungeons")["/api/forever/dungeons"]

    assert status == 200
    dungeons = {d["name_slug"]: d for d in body["dungeons"]}
    assert len(dungeons) == 31
    assert dungeons["deadmines"] == {"id": 10036, "name": "Deadmines", "name_slug": "deadmines", "icon": FALLBACK_ICON}


def test_one_dungeon_by_slug() -> None:
    routes = get_api_routes("/api/forever/dungeons/deadmines", "/api/forever/dungeons/nope")
    assert routes["/api/forever/dungeons/deadmines"][0] == 200
    assert routes["/api/forever/dungeons/nope"][0] == 404


def test_retail_serves_no_dungeons_while_none_have_an_id() -> None:
    status, body = get_api_routes("/api/retail/dungeons")["/api/retail/dungeons"]
    assert status == 200
    assert body == {"dungeons": []}
