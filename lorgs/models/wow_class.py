"""Playable (and some non playble) Classes in WoW."""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models.wow_actor import WowActor
from lorgs.models.wow_spell import WowSpell


if typing.TYPE_CHECKING:
    from lorgs.models.wow_spec import WowSpec


class WowClass(WowActor):
    """A playable class in wow."""

    id: int
    """int: class id, mostly used for sorting."""

    name: str
    """Human readable name. e.g. "Death Knight"."""

    color: str = ""
    """Hexadecimal color code. e.g. "#FF7C0A"."""

    @property
    def name_slug_cap(self) -> str:
        """PascalCase version of the Name. eg. "DeathKnight"."""
        return self.name.replace(" ", "")

    @property
    def name_slug(self) -> str:
        """Slugified version of the Name. eg. "deathknight"."""
        return utils.slug(self.name)

    @property
    def is_other(self) -> bool:
        """bool: flag for the trinkets/potions groups"""
        return self.name.lower() == "other"

    def __repr__(self) -> str:
        return f"<Class(name='{self.name}')>"

    def __lt__(self, other: "WowClass") -> bool:
        return self.id < other.id

    def as_dict(self) -> dict[str, typing.Any]:
        return {
            "name": self.name,
            "name_slug": self.name_slug,
            "specs": [spec.full_name_slug for spec in sorted(self.specs)],
            "spec_ids": [spec.id for spec in self.specs],
            "color": self.color,
        }

    @property
    def specs(self) -> set["WowSpec"]:
        from lorgs.models.wow_spec import WowSpec

        return {spec for spec in WowSpec.list() if spec.wow_class == self}

    ##########################
    # Methods
    #
    def add_spell(self, spell: typing.Optional[WowSpell] = None, **kwargs: typing.Any) -> WowSpell:
        kwargs.setdefault("spell_type", self.name_slug)
        kwargs.setdefault("color", self.color)
        return super().add_spell(spell, **kwargs)

    def add_buff(self, spell: typing.Optional[WowSpell] = None, **kwargs: typing.Any) -> WowSpell:
        kwargs.setdefault("spell_type", self.name_slug)
        kwargs.setdefault("color", self.color)
        return super().add_buff(spell, **kwargs)

    def add_debuff(self, spell: typing.Optional[WowSpell] = None, **kwargs: typing.Any) -> WowSpell:
        kwargs.setdefault("spell_type", self.name_slug)
        kwargs.setdefault("color", self.color)
        return super().add_debuff(spell, **kwargs)

    def add_event(self, event: typing.Optional[WowSpell] = None, **kwargs: typing.Any) -> WowSpell:
        kwargs.setdefault("spell_type", self.name_slug)
        kwargs.setdefault("color", self.color)
        return super().add_event(event, **kwargs)
