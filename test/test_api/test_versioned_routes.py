"""Seams: versioned routes live under `/api/{game_version}/`, global routes have no prefix."""

from __future__ import annotations

from test.helpers import get_api_routes


def test_each_game_version_serves_its_own_data() -> None:
    routes = get_api_routes("/api/retail/specs", "/api/mists/specs", "/api/forever/specs")
    slugs = {
        path: {spec["full_name_slug"] for spec in body["specs"]}
        for path, (status, body) in routes.items()
        if status == 200
    }

    assert len(slugs) == 3
    sizes = {path: len(found) for path, found in slugs.items()}
    assert sizes == {"/api/retail/specs": 44, "/api/mists/specs": 34, "/api/forever/specs": 27}


def test_the_same_boss_is_only_served_by_its_game_version() -> None:
    routes = get_api_routes(
        "/api/mists/bosses/the-stone-guard",
        "/api/retail/bosses/the-stone-guard",
        "/api/forever/bosses/the-stone-guard",
    )
    assert {path: status for path, (status, _) in routes.items()} == {
        "/api/mists/bosses/the-stone-guard": 200,
        "/api/retail/bosses/the-stone-guard": 404,
        "/api/forever/bosses/the-stone-guard": 404,
    }


def test_an_unknown_game_version_is_a_422() -> None:
    status, _ = get_api_routes("/api/classic/specs")["/api/classic/specs"]
    assert status == 422


def test_game_versions_are_an_enum_in_the_openapi_docs() -> None:
    status, body = get_api_routes("/api/openapi.json")["/api/openapi.json"]
    assert status == 200

    parameter = body["paths"]["/api/{game_version}/specs"]["get"]["parameters"][0]
    assert parameter["name"] == "game_version"
    schema = parameter["schema"]
    if "$ref" in schema:
        schema = body["components"]["schemas"][schema["$ref"].rsplit("/", 1)[-1]]
    assert schema["enum"] == ["retail", "mists", "forever"]


def test_global_routes_work_without_a_prefix() -> None:
    routes = get_api_routes("/api/game_versions", "/api/ping")
    assert {path: status for path, (status, _) in routes.items()} == {"/api/game_versions": 200, "/api/ping": 200}


def test_versioned_routes_are_not_reachable_without_a_prefix() -> None:
    paths = ["/api/specs", "/api/roles", "/api/zones", "/api/seasons/current", "/api/spec_ranking/mage-fire/some-boss"]
    routes = get_api_routes(*paths)
    assert {path: status for path, (status, _) in routes.items()} == dict.fromkeys(paths, 404)
