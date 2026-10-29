"""Seams: the mists GameData holds what the `MemoryModel` registry holds, and indexes it."""

from test.helpers import assert_game_data_matches_registry


def test_game_data_matches_registry() -> None:
    assert_game_data_matches_registry()


def test_game_data_is_the_package_game_data() -> None:
    from lorgs.data import GAME_DATA
    from lorgs.data.mists import MISTS_GAME_DATA
    from lorgs.game_version import MISTS
    from lorgs.models.game_data import get_game_data

    assert GAME_DATA is MISTS_GAME_DATA is get_game_data()
    assert GAME_DATA.game_version is MISTS


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


def test_bosses_are_found_by_slug_and_encounter_id() -> None:
    from lorgs.data import GAME_DATA

    assert GAME_DATA.bosses
    for boss in GAME_DATA.bosses:
        assert GAME_DATA.get_boss(full_name_slug=boss.full_name_slug) is boss
        assert GAME_DATA.get_boss(boss_id=boss.id) is boss


def test_spells_are_found_by_id_and_variation_id() -> None:
    from lorgs.data import GAME_DATA

    assert GAME_DATA.spells
    for spell in GAME_DATA.spells:
        for spell_id in (spell.spell_id, *spell.variations):
            assert spell in GAME_DATA.get_spells(spell_id)
