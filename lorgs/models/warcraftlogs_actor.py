from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import abc
import typing
from typing import ClassVar

# IMPORT THIRD PARTY LIBRARIES
import blinker

# IMPORT LOCAL LIBRARIES
from lorgs.models import base
from lorgs.models.warcraftlogs_cast import Cast  # noqa: TC001 # pydantic requires this import
from lorgs.models.wow_spell import SpellType, WowSpell


if typing.TYPE_CHECKING:
    from lorgs.models.warcraftlogs_fight import Fight
    from lorgs.models.wow_actor import WowActor


class BaseActor(base.BaseModel):
    """Base Class for any Actor in a Fight.

    these are usually either Players or NPC/Bosses

    """

    source_id: int = -1
    casts: list[Cast] = []

    _fight: Fight | None = None

    # Signal emitted by loaders when an actor load starts/succeeds/fails.
    event_actor_load: ClassVar[blinker.Signal] = blinker.signal("actor.load")

    def __hash__(self) -> int:

        if not self.fight:
            raise TypeError("Actor has no fight")
        if not self.fight.report:
            raise TypeError("Actor has no report")

        keys = (
            self.fight.report.report_id,
            self.fight.fight_id,
            self.source_id,
        )
        return hash(keys)

    ############################################################################
    #
    # Attributes
    #
    ############################################################################

    @property
    def fight(self) -> Fight | None:
        """Parent fight (private storage to avoid Pydantic schema resolution)."""
        return self._fight

    @fight.setter
    def fight(self, value: Fight) -> None:
        self._fight = value

    @property
    def _has_source_id(self) -> bool:
        return self.source_id >= 0

    @property
    def has_own_casts(self) -> bool:
        """Return true if a player has own casts (eg.: exclude raid wide buffs like bloodlust)."""
        for cast in self.casts:
            spell = WowSpell.get(spell_id=cast.spell_id)
            if spell and spell.spell_type != SpellType.BUFF:
                return True
        return False

    @abc.abstractmethod
    def get_actor_type(self) -> WowActor:
        """Get the Type of Actor."""

    @property
    def actor_type(self) -> WowActor:
        return self.get_actor_type()
