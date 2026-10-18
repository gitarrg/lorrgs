import sys
import unittest

import pytest
from lorgs.models import warcraftlogs_player
from lorgs.loaders.player_loader import PlayerLoader
from lorgs.models.warcraftlogs_player import Player

from lorgs.clients import wcl

from test import helpers
from test.test_models.test_warcraftlogs_fight import FIGHT_START, _fight, _fight_in_report


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = warcraftlogs_player.Player()
        self.loader = PlayerLoader(self.player)

    def test__set_source_id_from_events(self) -> None:
        events = [
            wcl.ReportEvent(type="something else", sourceID=2),
            wcl.ReportEvent(type="cast", sourceID=4),
            wcl.ReportEvent(type="cast", sourceID=8),
        ]

        self.player.source_id = -2
        self.loader._set_source_id_from_events(events)
        assert self.player.source_id == 4


def test_deaths_are_fight_relative() -> None:
    player = Player(source_id=7, name="Fallen")
    player.fight = _fight_in_report()

    player.process_death_events([
        wcl.DeathEvent(
            id=7,
            name="Fallen",
            type="Druid",
            deathTime=25_000,
            ability={"name": "Smash", "abilityIcon": "smash.jpg"},
        ),
    ])

    assert player.deaths == [{"ts": 4_000, "spell_name": "Smash", "spell_icon": "smash.jpg"}]


def test_deaths_raise_when_the_fight_has_no_report() -> None:
    player = Player(source_id=7, name="Fallen")
    player.fight = _fight(start_time=FIGHT_START)

    with pytest.raises(ValueError, match="Missing Parent Report"):
        player.process_death_events([
            wcl.DeathEvent(
                id=7,
                name="Fallen",
                type="Druid",
                deathTime=25_000,
                ability={"name": "Smash", "abilityIcon": "smash.jpg"},
            ),
        ])

    assert player.deaths == []


def _resurrect_query() -> dict:
    return helpers.wrap_data(
        [{
            "timestamp": 25_000,
            "type": "resurrect",
            "sourceID": 3,
            "targetID": 10,
            "abilityGameID": 20484,
        }],
        "report",
        "events",
        "data",
    )


def test_resurrections_are_fight_relative() -> None:
    player = Player(source_id=10, name="Caster")
    player.fight = _fight_in_report()

    PlayerLoader(player).process_query_result(_resurrect_query())

    assert player.resurrects[0]["ts"] == 4_000


def test_resurrections_raise_when_the_fight_has_no_report() -> None:
    player = Player(source_id=10, name="Caster")
    player.fight = _fight(start_time=FIGHT_START)

    with pytest.raises(ValueError, match="Missing Parent Report"):
        PlayerLoader(player).process_query_result(_resurrect_query())

    assert player.resurrects == []


if __name__ == "__main__":
    pytest.main(sys.argv)
