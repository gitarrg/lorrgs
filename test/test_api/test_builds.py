import pytest

from lorgs.models import spec_builds
from test.helpers import get_api_routes


def test_spec_without_builds_returns_an_empty_list(monkeypatch):
    monkeypatch.setattr(spec_builds.SpecBuilds, "get", classmethod(lambda cls, **kwargs: None))

    status, body = get_api_routes("/api/retail/builds/priest-shadow")["/api/retail/builds/priest-shadow"]

    assert status == 200
    assert body["builds"] == []
    assert body["settings"]["threshold"] == spec_builds.START_THRESHOLD


def test_stored_builds_are_served(monkeypatch):
    stored = spec_builds.SpecBuilds(
        game_version="retail",
        spec_slug="priest-shadow",
        fights=10,
        other=1,
        settings=spec_builds.BuildSettings(threshold=2, ignore=[5]),
        builds=[spec_builds.Build(letter="A", fights=9, hero_tree="voidweaver", talents={1: 1})],
    )
    monkeypatch.setattr(spec_builds.SpecBuilds, "get", classmethod(lambda cls, **kwargs: stored))

    status, body = get_api_routes("/api/retail/builds/priest-shadow")["/api/retail/builds/priest-shadow"]

    assert status == 200
    assert body["fights"] == 10
    assert body["settings"]["threshold"] == 2
    assert body["settings"]["ignore"] == [5]
    assert body["builds"][0]["letter"] == "A"
    assert "updated" not in body


@pytest.mark.parametrize(
    "path",
    [
        "/api/retail/builds/no-such-spec",
        "/api/retail/builds/other-trinkets",
        "/api/mists/builds/monk-windwalker",
    ],
)
def test_unknown_or_unsupported_spec_is_404(path):
    status, _ = get_api_routes(path)[path]
    assert status == 404
