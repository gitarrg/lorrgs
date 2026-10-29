"""Seams: the forever GameData holds what the `MemoryModel` registry holds, and indexes it."""

from test.helpers import assert_game_data_matches_registry


def test_game_data_matches_registry() -> None:
    assert_game_data_matches_registry()


def test_game_data_is_the_package_game_data() -> None:
    from lorgs.data import GAME_DATA
    from lorgs.game_version import FOREVER

    assert GAME_DATA is FOREVER.data


def test_specs_are_found_by_slug() -> None:
    from lorgs.data import GAME_DATA

    assert len(GAME_DATA.specs_by_slug) == len(GAME_DATA.specs)
    for spec in GAME_DATA.specs:
        assert GAME_DATA.get_spec(spec.full_name_slug) is spec


def test_back_references() -> None:
    from lorgs.data import GAME_DATA

    for spec in GAME_DATA.specs:
        assert spec in spec.role.specs
        assert spec in spec.wow_class.specs
    for zone in GAME_DATA.zones:
        assert all(boss.zone is zone for boss in zone.bosses)
