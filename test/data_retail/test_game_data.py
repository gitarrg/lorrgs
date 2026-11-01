"""Seams: the retail GameData indexes the objects its package defines."""


def test_game_data_is_the_package_game_data() -> None:
    from lorgs.data.retail import GAME_DATA
    from lorgs.data import RETAIL

    assert GAME_DATA is RETAIL.data


def test_specs_are_found_by_slug() -> None:
    from lorgs.data.retail import GAME_DATA

    assert len(GAME_DATA.specs_by_slug) == len(GAME_DATA.specs)
    for spec in GAME_DATA.specs:
        assert GAME_DATA.get_spec(spec.full_name_slug) is spec


def test_back_references() -> None:
    from lorgs.data.retail import GAME_DATA

    for spec in GAME_DATA.specs:
        assert spec in spec.role.specs
        assert spec in spec.wow_class.specs
    for zone in GAME_DATA.zones:
        assert all(boss.zone is zone for boss in zone.bosses)


def test_bosses_are_found_by_slug_and_encounter_id() -> None:
    from lorgs.data.retail import GAME_DATA

    for boss in GAME_DATA.bosses:
        assert GAME_DATA.get_boss(full_name_slug=boss.full_name_slug) is boss
    assert GAME_DATA.get_boss(boss_id=GAME_DATA.bosses[0].id) is not None


def test_spells_are_found_by_id_and_variation_id() -> None:
    from lorgs.data.retail import GAME_DATA

    for spell in GAME_DATA.spells:
        for spell_id in (spell.spell_id, *spell.variations):
            assert spell in GAME_DATA.get_spells(spell_id)


def test_no_object_is_in_two_collections() -> None:
    from lorgs.data.retail import GAME_DATA

    collections = [
        GAME_DATA.roles,
        GAME_DATA.classes,
        GAME_DATA.specs,
        GAME_DATA.zones,
        GAME_DATA.bosses,
        GAME_DATA.dungeons,
        [GAME_DATA.season],
        GAME_DATA.spells,
    ]
    ids = [id(obj) for objects in collections for obj in objects]
    assert len(ids) == len(set(ids))


def test_specs_hold_only_trinkets_of_the_current_season() -> None:
    from lorgs.data.retail import GAME_DATA
    from lorgs.data.expansions.legion.dungeons.halls_of_valor import HORN_OF_VALOR
    from lorgs.models.wow_trinket import WowTrinket

    season_trinkets = list(GAME_DATA.season.trinkets)
    assert season_trinkets
    for spec in GAME_DATA.specs:
        for spell in spec.all_spells:
            if isinstance(spell, WowTrinket):
                assert spell in season_trinkets, f"{spec.full_name_slug}: {spell.name}"
    for trinket in season_trinkets:
        assert all(trinket in spec.spells for spec in trinket.specs)

    assert HORN_OF_VALOR.specs, "an older trinket still names its specs"
    assert not any(HORN_OF_VALOR in spec.spells for spec in HORN_OF_VALOR.specs)
