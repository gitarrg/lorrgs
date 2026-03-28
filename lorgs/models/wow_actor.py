from __future__ import annotations

# IMPORT STANDARD LIBRARIES
from typing import Any, Optional

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base
from lorgs.models.wow_spell import WowSpell


class WowActor(base.MemoryModel):
    """Base Class for any actor type in the game.

    Subclases can be playable specs or npc/bosses.
    Essentially anything that can cast spells or have buffs/debuffs applied.

    """

    spells: list[WowSpell] = []
    buffs: list[WowSpell] = []
    debuffs: list[WowSpell] = []
    events: list[WowSpell] = []

    parents: list["WowActor"] = []
    """List of Parent Types. eg.: Classes are parents of Specs."""

    @property
    def full_name_slug(self) -> str:
        return ""

    @property
    def all_spells(self) -> list[WowSpell]:
        """Get all spells actor can use."""
        spells = [p.all_spells for p in self.parents] + [self.spells]
        return utils.flatten(spells)

    @property
    def all_buffs(self) -> list[WowSpell]:
        """Get all buffs that are relavent for this actor."""
        buffs = [p.all_buffs for p in self.parents] + [self.buffs]
        return utils.flatten(buffs)

    @property
    def all_debuffs(self) -> list[WowSpell]:
        """Get all debuffs that are relavent for this actor."""
        debuffs = [p.all_debuffs for p in self.parents] + [self.debuffs]
        return utils.flatten(debuffs)

    @property
    def all_events(self) -> list[WowSpell]:
        """Get all events that are relavent for this actor."""
        events = [p.all_events for p in self.parents] + [self.events]
        return utils.flatten(events)

    ##########################
    # Methods
    #
    def add_spell(self, spell: Optional[WowSpell] = None, **kwargs: Any) -> WowSpell:
        """Add a spell to the actor."""
        if not spell:
            kwargs.setdefault("event_type", "cast")
            kwargs.setdefault("spell_type", self.full_name_slug)
            spell = WowSpell(**kwargs)

        self.spells.append(spell)
        return spell

    def add_spells(self, *spells: WowSpell) -> None:
        """Add multiple spells to the actor."""
        self.spells.extend(spells)

    def add_buff(self, spell: Optional[WowSpell] = None, **kwargs) -> WowSpell:
        """Add a buff to the actor."""
        if not spell:
            kwargs.setdefault("event_type", "applybuff")
            kwargs.setdefault("spell_type", self.full_name_slug)
            spell = WowSpell(**kwargs)
        else:
            spell = spell.model_copy(update={"event_type": "applybuff"})

        self.buffs.append(spell)
        return spell

    def add_buffs(self, *spells: WowSpell) -> None:
        """Add multiple buffs to the actor."""
        self.buffs.extend(spells)

    def add_debuff(self, spell: Optional[WowSpell] = None, **kwargs) -> WowSpell:
        """Add a debuff to the actor."""
        if not spell:
            kwargs.setdefault("event_type", "applydebuff")
            kwargs.setdefault("spell_type", self.full_name_slug)
            spell = WowSpell(**kwargs)

        self.debuffs.append(spell)
        return spell

    def add_debuffs(self, *spells: WowSpell) -> None:
        """Add multiple debuffs to the actor."""
        self.debuffs.extend(spells)

    def add_event(self, event: Optional[WowSpell] = None, **kwargs: Any) -> WowSpell:
        """Add a custom event to the actor."""
        if not event:
            kwargs.setdefault("spell_type", self.full_name_slug)
            event = WowSpell(**kwargs)

        self.events.append(event)
        return event

    def add_events(self, *spells: WowSpell) -> None:
        """Add multiple events to the actor."""
        self.events.extend(spells)
