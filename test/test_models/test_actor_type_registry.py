"""The Game Data finds Actor Types with behaviour of their own like any other."""

from lorgs.models.raid_boss import RaidBoss
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_role import WowRole
from lorgs.models.wow_spec import WowSpec
from test.helpers import game_data_with


class RestorationDruid(WowSpec):
    """Spec Actor Type with behaviour of its own."""


def test_subclassed_spec_is_found_in_the_game_data() -> None:
    role = WowRole(id=90001, name="Registry Probe Healer", code="registry-probe-heal")
    wow_class = WowClass(id=90001, name="Registry Probe Class")
    spec = RestorationDruid(
        name="Registry Probe Restoration",
        role=role,
        wow_class=wow_class,
    )
    game_data = game_data_with(specs=[spec])

    assert game_data.get_spec(spec.full_name_slug) is spec


class Nekzali(RaidBoss):
    """Boss Actor Type with behaviour of its own."""


def test_subclassed_boss_is_found_in_the_game_data() -> None:
    boss = Nekzali(id=90002, name="Registry Probe Nekzali")
    game_data = game_data_with(bosses=[boss])

    assert game_data.get_boss(boss_id=90002) is boss
    assert game_data.get_boss(full_name_slug=boss.full_name_slug) is boss
