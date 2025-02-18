"""Defines an Encounter/RaidBoss in the Game.."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing
from typing import Any

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models.wow_actor import WowActor
from lorgs.models.wow_spell import WowSpell
from lorgs.models.wow_trinket import WowTrinket


class Phase(WowSpell):

    name: str = "P{:d}"

    event_type: str
    """WCL Event Type (`applybuff`, `removebuff`, etc)"""

    count: int = 0
    """Only trigger if its the n'th count of the event.
    
    if 0: trigger a new phase each time the event occurs
    """


class RaidBoss(WowActor):
    """A raid boss in the Game."""

    id: int
    """The Encounter ID."""

    name: str = ""
    """Full Name of the Boss (eg.: "Halondrus the Reclaimer")."""

    nick: str = ""
    """Short commonly used Nickname. eg.: "Halondrus"."""

    icon: str = ""
    """Name of the Icon file. eg.: ``"inv_achievement_raid_progenitorraid_progenium_keeper.jpg"``"""

    trinkets: list[WowTrinket] = []
    """Trinkets which can drop from this Boss."""

    phases: list[Phase] = []
    """Phase triggers"""

    def __repr__(self):
        return f"<RaidBoss(id={self.id} name={self.name})>"

    # alias
    def add_cast(self, *args: Any, **kwargs: Any) -> WowSpell:
        return self.add_spell(*args, **kwargs)

    def add_trinket(self, **kwargs: Any) -> WowTrinket:
        trinket = WowTrinket(**kwargs)
        self.trinkets.append(trinket)
        return trinket

    def add_phase(self, **kwargs: typing.Any) -> Phase:
        phase = Phase(**kwargs)
        self.phases.append(phase)
        return phase

    @property
    def name_slug(self) -> str:
        """Complete Name slugified. eg.: `"halondrus-the-reclaimer"`."""
        return utils.slug(self.name, space="-")

    # Alias to maintain the Actor-Interface
    @property
    def full_name_slug(self) -> str:
        return self.name_slug

    def as_dict(self) -> dict[str, typing.Any]:
        return {
            "id": self.id,
            # renames to match the "Actor"-Interface
            "name": self.nick or self.name,
            "icon": self.icon,
            "full_name": self.name,
            "full_name_slug": self.name_slug,
        }
