"""Defines an Encounter/RaidBoss in the Game.."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing
from enum import Enum
from typing import Any

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models.wow_actor import WowActor
from lorgs.models.wow_trinket import WowTrinket


if typing.TYPE_CHECKING:
    from lorgs.clients import wcl
    from lorgs.models.warcraftlogs_fight import Phase
    from lorgs.models.wow_spell import WowSpell


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

    class PhaseType(Enum):
        """Type of phases for a boss."""

        STATIC = "static"
        DYNAMIC = "dynamic"

    phase_type: PhaseType = PhaseType.STATIC
    """Type of phases for this boss."""

    def post_init(self) -> None:
        super().post_init()
        # Subclasses are stored under their own type; also index them as RaidBoss
        # so RaidBoss.get() / list() still find them.
        if type(self) is not RaidBoss:
            self.__instances__[RaidBoss].add(self)

    def __repr__(self):
        return f"<RaidBoss(id={self.id} name={self.name})>"

    # alias
    def add_cast(self, *args: Any, **kwargs: Any) -> WowSpell:
        return self.add_spell(*args, **kwargs)

    def add_trinket(self, **kwargs: Any) -> WowTrinket:
        trinket = WowTrinket(**kwargs)
        self.trinkets.append(trinket)
        return trinket

    def phase_from_transition(self, transition: wcl.PhaseTransition) -> Phase | None:  # ruff: ignore[no-self-use]
        """Map a WCL phase transition into a fight Phase.

        Returns None if this transition should be skipped.
        """
        # inlined to avoid a cycle: Fight -> Boss -> RaidBoss
        from lorgs.models.warcraftlogs_fight import Phase  # ruff: ignore[import-outside-top-level]

        if transition.startTime <= 100:  # skip pull as phase
            return None

        return Phase(ts=transition.startTime, phase_id=transition.id)

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
            "phase_type": self.phase_type.value,
        }
