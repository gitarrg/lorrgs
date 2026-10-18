
import unittest
from unittest import mock

from lorgs.models.warcraftlogs_comp_ranking import get_composition


def create_fake_player(role="", spec="", **kwargs):
    player = mock.MagicMock(**kwargs)
    player.spec.role.code = role
    player.spec.full_name_slug = spec
    return player


FAKE_PLAYERS = [
    create_fake_player(role="tank", spec="specA"),
    create_fake_player(role="tank", spec="specB"),
    create_fake_player(role="heal", spec="specA"),
    create_fake_player(role="mdps", spec="specC"),
    create_fake_player(role="rdps", spec="specB"),
]


class TestGetComposition(unittest.TestCase):

    def test_empty(self):
        """Test an empty Comp."""
        result = get_composition(players=[])
        expected = {"roles": {}, "specs": {}, "classes": {}}
        assert result == expected

    def test_roles(self):
        """Verify roles get calculated correctly."""
        result = get_composition(players=FAKE_PLAYERS)
        result_roles = result["roles"]
        assert result_roles["tank"] == 2
        assert result_roles["heal"] == 1
        assert result_roles["mdps"] == 1
        assert result_roles["rdps"] == 1

    def test_specs(self):
        """Verify specs get calculated correctly."""
        result = get_composition(players=FAKE_PLAYERS)
        result_specs = result["specs"]
        assert result_specs["specA"] == 2
        assert result_specs["specB"] == 2
        assert result_specs["specC"] == 1
