import sys
import unittest

import pytest

from lorgs.models.warcraftlogs_cast import Cast, process_auras, process_until_events
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.game_data import GameData
from lorgs.models.season import Season
from lorgs.models.wow_spell import WowSpell


def _game_data(*spells: WowSpell) -> GameData:
    season = Season(name="Test", ilvl=1)
    return GameData(roles=[], classes=[], seasons=[season], current_season=season, difficulties=(RaidDifficulty.HEROIC,), spells=list(spells))


class Test_Cast(unittest.TestCase):
    """Test the Custom process event logic."""

    ############################################################################
    # Process Aura
    #

    def test__process_auras__calc_buff_duration(self):
        events = [
            Cast(spell_id=10, timestamp=100, event_type="applybuff"),
            Cast(spell_id=10, timestamp=250, event_type="removebuff"),
        ]
        expected = [Cast(spell_id=10, timestamp=100, duration=150, event_type="applybuff")]

        result = process_auras(events, _game_data())
        assert result == expected

    def test__process_auras__multiple_applications(self):
        events = [
            Cast(spell_id=10, timestamp=110, event_type="applybuff"),
            Cast(spell_id=10, timestamp=120, event_type="applybuff"),
            Cast(spell_id=10, timestamp=130, event_type="applybuff"),
            Cast(spell_id=10, timestamp=250, event_type="removebuff"),
        ]
        expected = [Cast(spell_id=10, timestamp=110, duration=140, event_type="applybuff")]

        result = process_auras(events, _game_data())
        assert len(result) == 1  # the removebuff event should be dropped
        assert result == expected

    def test__process_auras__multiple_buffs_same_spell(self):
        events = [
            Cast(spell_id=10, timestamp=100, event_type="applybuff"),
            Cast(spell_id=10, timestamp=150, event_type="removebuff"),
            Cast(spell_id=10, timestamp=200, event_type="applybuff"),
            Cast(spell_id=10, timestamp=260, event_type="removebuff"),
        ]
        expected = [
            Cast(spell_id=10, timestamp=100, event_type="applybuff", duration=50),
            Cast(spell_id=10, timestamp=200, event_type="applybuff", duration=60),
        ]

        result = process_auras(events, _game_data())
        assert len(result) == 2  # the removebuff event should be dropped
        assert result == expected

    def test__process_auras__multiple_buffs_diff_spell(self):
        events = [
            Cast(spell_id=10, timestamp=100, event_type="applybuff"),
            Cast(spell_id=20, timestamp=120, event_type="applybuff"),
            Cast(spell_id=10, timestamp=150, event_type="removebuff"),
            Cast(spell_id=20, timestamp=260, event_type="removebuff"),
        ]
        expected = [
            Cast(spell_id=10, timestamp=100, event_type="applybuff", duration=50),  # 100 - 150
            Cast(spell_id=20, timestamp=120, event_type="applybuff", duration=140),  # 120 - 260
        ]

        result = process_auras(events, _game_data())
        assert len(result) == 2
        assert result == expected

    def test__process_auras__automatic_start(self) -> None:
        events = [
            # Aura fading 4sec into fight
            Cast(spell_id=10, timestamp=4000, event_type="removebuff"),
        ]

        # the spell has 6sec as its default duration
        result = process_auras(events, _game_data(WowSpell(spell_id=10, duration=6)))

        assert len(result) == 1  # still one entry
        event = result[0]
        assert event.timestamp == -2000
        assert event.event_type == "applybuff"
        assert event == Cast(spell_id=10, timestamp=-2000, event_type="applybuff")

    def test__process_auras__second_apply_without_remove_is_dropped(self) -> None:
        """A second apply of an already active aura is dropped until it is removed."""
        events = [
            Cast(spell_id=10, timestamp=1000, event_type="applybuff"),
            Cast(spell_id=10, timestamp=5000, event_type="applybuff"),
        ]

        result = process_auras(events, _game_data())

        assert result == [Cast(spell_id=10, timestamp=1000, event_type="applybuff")]

    ############################################################################
    # Process Until Events
    #

    def test_process_until_events(self) -> None:
        # Arrange some test abilities
        until_event = WowSpell(spell_id=200)
        spell = WowSpell(spell_id=100, until=until_event)

        # test event data
        events = [
            Cast(spell_id=100, timestamp=2000),
            Cast(spell_id=200, timestamp=3250),
        ]

        # run
        result = process_until_events(events, _game_data(spell, until_event))
        assert len(result) == 1
        cast = result[0]
        assert cast.timestamp == 2000  # make sure its the first event
        assert cast.duration == 1250

    def test_process_until_events_multipleA(self) -> None:
        # Arrange some test abilities
        until_event = WowSpell(spell_id=200)
        spell = WowSpell(spell_id=100, until=until_event)

        # test event data
        events = [
            Cast(spell_id=100, timestamp=200),  # < start #1
            Cast(spell_id=200, timestamp=450),  # duration = 250
            Cast(spell_id=100, timestamp=500),  # < start #2
            Cast(spell_id=200, timestamp=610),  # duration = 110
        ]

        # run
        result = process_until_events(events, _game_data(spell, until_event))

        # validate
        expected = [
            Cast(spell_id=100, timestamp=200, duration=250),
            Cast(spell_id=100, timestamp=500, duration=110),
        ]
        assert result == expected

    def test_process_until_events_multipleB(self) -> None:
        # Arrange some test abilities
        until_event = WowSpell(spell_id=200)
        spell = WowSpell(spell_id=100, until=until_event)

        # test event data
        events = [
            Cast(spell_id=100, timestamp=200),
            Cast(spell_id=100, timestamp=300),
            Cast(spell_id=200, timestamp=450),  # duration = 250
            Cast(spell_id=200, timestamp=610),  # duration = 310
        ]

        # run
        result = process_until_events(events, _game_data(spell, until_event))

        # validate
        expected = [
            Cast(spell_id=100, timestamp=200, duration=250),
            Cast(spell_id=100, timestamp=300, duration=310),
        ]
        assert result == expected


if __name__ == "__main__":
    pytest.main(sys.argv)
