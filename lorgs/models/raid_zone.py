"""Defines a Raid in the Game."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.wow_trinket import WowTrinket


# pylint: disable=too-few-public-methods


class RaidZone(base.MemoryModel):
    """A raid zone in the Game."""

    id: int | float
    """ID of the Raid Zone. aka. T28, T29 (as used in WarcraftLogs).
    
    Multi raid tiers can use floats. eg. 46.1, 46.2
    """

    name: str
    """Full Name of the Zone. eg.: `Castle Nathria`."""

    bosses: list[RaidBoss] = []
    """All Bosses, in order, in this Zone."""

    icon: str = ""
    """The name of the Icon for this RaidZone."""

    trinkets: list[WowTrinket] = []

    @property
    def name_slug(self) -> str:
        return utils.slug(self.name, space="-")

    def __repr__(self) -> str:
        return f"<RaidZone(id={self.id} name={self.name})>"

    def as_dict(self) -> dict[str, typing.Any]:
        return {
            "id": self.id,
            "name": self.name,
            "name_slug": self.name_slug,
            "icon": self.icon,
            "bosses": [boss.as_dict() for boss in self.bosses],
        }

    def add_boss(self, boss: typing.Optional[RaidBoss] = None, **kwargs: typing.Any) -> RaidBoss:
        """Add a new RaidBoss to this zone."""
        boss = boss or RaidBoss(**kwargs)
        self.bosses.append(boss)
        return boss

    def add_bosses(self, *bosses: RaidBoss) -> None:
        """Add multiple Bosses to this Zone."""
        self.bosses.extend(bosses)
