"""Models for Classes, Specs, Spells and Roles."""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models.wow_actor import WowActor
from lorgs.models.wow_class import WowClass  # ruff: ignore[typing-only-first-party-import] pydantic required
from lorgs.models.wow_role import WowRole  # ruff: ignore[typing-only-first-party-import]
from lorgs.models.wow_spell import WowSpell  # ruff: ignore[typing-only-first-party-import]


class WowSpec(WowActor):
    """docstring for Spec."""

    id: int = 0
    """Blizzard specialization id (ChrSpecialization.ID).
    Zero for utility specs (e.g. Other)."""

    index: int = 0
    """Index of the Spec (1-4)."""

    name: str

    role: WowRole

    wow_class: WowClass

    short_name: str = ""
    """Short Version of the Name. eg.: "Prot" or "Resto". Defaults to `self.name`"""

    def post_init(self) -> None:
        self.parents.append(self.wow_class)
        self.wow_class.register_spec(self)
        return super().post_init()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"

    def __repr__(self) -> str:
        return str(self)

    @property
    def name_slug(self) -> str:
        """Slugified Version of the Name. eg.: "beastmastery"."""
        return utils.slug(self.name)

    @property
    def name_slug_cap(self) -> str:
        """PascalCase version. eg.: "BeastMastery."""
        return self.name.replace(" ", "")

    @property
    def full_name(self) -> str:
        """Complete Name including the parent Class. eg.: "Havoc Demon Hunter"."""
        return f"{self.name} {self.wow_class.name}"

    @property
    def full_name_slug(self) -> str:
        """Slugified version of the full name. eg.: "demonhunter-havoc"."""
        return f"{self.wow_class.name_slug}-{self.name_slug}"

    def __lt__(self, other: WowSpec) -> bool:
        def sort_key(obj: WowSpec) -> tuple[WowRole, WowClass, str]:
            return (obj.role, obj.wow_class, obj.name)

        return sort_key(self) < sort_key(other)

    def as_dict(self) -> dict[str, typing.Any]:
        return {
            "id": self.id,
            "index": self.index,
            "name": self.name,
            "full_name": self.full_name,
            "full_name_slug": self.full_name_slug,
            "role": self.role.code,
            "class": {
                "name": self.wow_class.name,  # required for the WCL-Header Link
                "name_slug": self.wow_class.name_slug,
            },
        }

    ##########################
    # Methods
    #
    def add_spell(self, spell: WowSpell | None = None, **kwargs: typing.Any) -> WowSpell:
        kwargs.setdefault("color", self.wow_class.color)
        return super().add_spell(spell, **kwargs)

    def add_buff(self, spell: WowSpell | None = None, **kwargs) -> WowSpell:
        kwargs.setdefault("color", self.wow_class.color)
        return super().add_buff(spell, **kwargs)

    def add_debuff(self, spell: WowSpell | None = None, **kwargs) -> WowSpell:
        kwargs.setdefault("color", self.wow_class.color)
        return super().add_debuff(spell, **kwargs)

    def add_event(self, event: WowSpell | None = None, **kwargs: typing.Any) -> WowSpell:
        kwargs.setdefault("color", self.wow_class.color)
        return super().add_event(event, **kwargs)
