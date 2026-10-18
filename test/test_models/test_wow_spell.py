import sys
import unittest

import pytest

from lorgs.models.wow_spell import WowSpell, build_spell_query


################################################################################


def test_spell_ids():

    spells = [WowSpell(spell_id=5), WowSpell(spell_id=3), WowSpell(spell_id=10)]

    result = WowSpell.spell_ids(spells)
    assert result == [3, 5, 10]


def test_spell_ids_str():

    spells = [WowSpell(spell_id=5), WowSpell(spell_id=3), WowSpell(spell_id=10)]

    result = WowSpell.spell_ids_str(spells)
    assert result == "3,5,10"


################################################################################


class TestBuildQuery:
    def test_build_query_empty(self) -> None:

        result = build_spell_query()
        assert result == ""

    def test_build_query_check_type(self) -> None:

        spell = WowSpell(spell_id=10, event_type="foo")

        result = build_spell_query(spell)
        assert result == "(type='foo' and ability.id in (10))"

    def test_build_query__multiple_spells_same_type(self) -> None:

        spells = [
            WowSpell(spell_id=10, event_type="foo"),
            WowSpell(spell_id=30, event_type="foo"),
            WowSpell(spell_id=20, event_type="foo"),
        ]

        result = build_spell_query(*spells)
        assert result == "(type='foo' and ability.id in (10,20,30))"

    def test_build_query__multiple_spells_diff_type(self) -> None:

        spells = [
            WowSpell(spell_id=10, event_type="foo"),
            WowSpell(spell_id=30, event_type="bar"),
            WowSpell(spell_id=20, event_type="foo"),
        ]

        expected = "(type='foo' and ability.id in (10,20)) or (type='bar' and ability.id in (30))"

        result = build_spell_query(*spells)
        assert result == expected

    def test_build_query__aura_type(self) -> None:
        """Buffs and debuffs also query the matching remove event."""

        spell = WowSpell(spell_id=10, event_type="applybuff")

        expected = "(type='applybuff' and ability.id in (10)) or (type='removebuff' and ability.id in (10))"

        result = build_spell_query(spell)
        assert result == expected


if __name__ == "__main__":
    pytest.main(sys.argv)
