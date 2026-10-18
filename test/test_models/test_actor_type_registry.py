"""Looking up an Actor Type finds instances of its subclasses."""

from lorgs.models.raid_boss import RaidBoss
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_role import WowRole
from lorgs.models.wow_spec import WowSpec


class RestorationDruid(WowSpec):
    """Spec Actor Type with behaviour of its own."""


def test_subclassed_spec_is_found_via_wow_spec() -> None:
    role = WowRole(id=90001, name="Registry Probe Healer", code="registry-probe-heal")
    wow_class = WowClass(id=90001, name="Registry Probe Class")
    spec = RestorationDruid(
        name="Registry Probe Restoration",
        role=role,
        wow_class=wow_class,
    )

    assert WowSpec.get(name="Registry Probe Restoration") is spec
    assert [item for item in WowSpec.list() if item is spec] == [spec]


class Nekzali(RaidBoss):
    """Boss Actor Type with behaviour of its own."""


def test_subclassed_boss_is_found_via_raid_boss() -> None:
    boss = Nekzali(id=90002, name="Registry Probe Nekzali")

    assert RaidBoss.get(id=90002) is boss
    assert [item for item in RaidBoss.list() if item is boss] == [boss]
