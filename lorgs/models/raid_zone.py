"""Defines a Raid in the Game."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.wow_trinket import WowTrinket


# pylint: disable=too-few-public-methods

AUTO_DIFFICULTY = "auto"
"""Difficulty token (in URLs, routes and task payloads) that stands for the zone's `RaidZone.difficulty`."""


class RaidZone(base.StaticModel):
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

    difficulty: RaidDifficulty | None = None
    """The one difficulty we rank in this Zone. eg.: Heroic, as the only difficulty with 25-man logs.

    `None` lets the user pick from the Game Version's difficulties.
    """

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
            "difficulty": self.difficulty.name.lower() if self.difficulty else None,
            "bosses": [boss.as_dict() for boss in self.bosses],
        }

    def add_boss(self, boss: RaidBoss | None = None, **kwargs: typing.Any) -> RaidBoss:
        """Add a new RaidBoss to this zone."""
        boss = boss or RaidBoss(**kwargs)
        self.bosses.append(boss)
        return boss

    def add_bosses(self, *bosses: RaidBoss) -> None:
        """Add multiple Bosses to this Zone."""
        self.bosses.extend(bosses)
