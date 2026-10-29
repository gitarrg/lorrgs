"""Seams: one process holds the Game Data of every Game Version, and their lookups don't mix."""

from __future__ import annotations

from lorgs.data import FOREVER, GAME_VERSIONS, MISTS, RETAIL


def test_every_game_version_is_loaded() -> None:
    assert list(GAME_VERSIONS) == ["retail", "mists", "forever"]
    assert [version.data for version in GAME_VERSIONS.values()] == [RETAIL.data, MISTS.data, FOREVER.data]


def test_the_same_spec_slug_resolves_to_a_different_object_per_game_version() -> None:
    slug = "mage-fire"
    retail_spec = RETAIL.data.get_spec(slug)
    mists_spec = MISTS.data.get_spec(slug)

    assert retail_spec is not None
    assert mists_spec is not None
    assert retail_spec is not mists_spec
    assert retail_spec.wow_class is not mists_spec.wow_class
    assert retail_spec.role is not mists_spec.role


def test_game_data_objects_have_one_owner() -> None:
    owned = {name: {id(spec) for spec in version.data.specs} for name, version in GAME_VERSIONS.items()}
    names = list(owned)
    for i, first in enumerate(names):
        for second in names[i + 1 :]:
            assert not owned[first] & owned[second], f"{first} and {second} share specs"


def test_back_references_stay_inside_their_game_version() -> None:
    for version in GAME_VERSIONS.values():
        specs = {id(spec) for spec in version.data.specs}
        for role in version.data.roles:
            assert {id(spec) for spec in role.specs} <= specs
        for zone in version.data.zones:
            assert all(boss.zone is zone for boss in zone.bosses)


def test_lookups_only_find_their_own_game_version() -> None:
    assert FOREVER.data.get_boss(full_name_slug="the-stone-guard") is None
    assert MISTS.data.get_boss(full_name_slug="the-stone-guard") is not None
    assert RETAIL.data.get_boss(full_name_slug="the-stone-guard") is None
