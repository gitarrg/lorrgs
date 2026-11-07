"""Forever's dungeons are served for User Reports (never ranked)."""

from __future__ import annotations

from test.helpers import get_api_routes

from lorgs.models.dungeon import FALLBACK_ICON


def test_dungeons_are_listed_with_the_fallback_icon() -> None:
    status, body = get_api_routes("/api/forever/dungeons")["/api/forever/dungeons"]

    assert status == 200
    dungeons = {d["name_slug"]: d for d in body["dungeons"]}
    assert len(dungeons) == 31
    assert dungeons["deadmines"] == {"id": 10036, "name": "Deadmines", "name_slug": "deadmines", "icon": FALLBACK_ICON, "par_time": 0}


def test_one_dungeon_by_slug() -> None:
    routes = get_api_routes("/api/forever/dungeons/deadmines", "/api/forever/dungeons/nope")
    assert routes["/api/forever/dungeons/deadmines"][0] == 200
    assert routes["/api/forever/dungeons/nope"][0] == 404


def test_retail_serves_the_dungeons_of_the_season() -> None:
    status, body = get_api_routes("/api/retail/dungeons")["/api/retail/dungeons"]
    assert status == 200
    dungeons = body["dungeons"]
    assert len(dungeons) == 8
    assert all(d["id"] and d["icon"] != "inv_misc_map_01.jpg" for d in dungeons)
