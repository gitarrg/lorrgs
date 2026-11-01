from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT THIRD PARTY LIBRARIES
import pydantic

# IMPORT LOCAL LIBRARIES
from lorgs.models import wow_item
from lorgs.models.wow_spell import SpellType


if typing.TYPE_CHECKING:
    from lorgs.models.wow_spec import WowSpec


class WowTrinket(wow_item.WowItem):
    """OnUse Trinkets."""

    spell_type: str = SpellType.TRINKET

    color: str = "#a335ee"  # Epic Items

    _specs: list[WowSpec] = pydantic.PrivateAttr(default_factory=list)

    @property
    def specs(self) -> list[WowSpec]:
        """Specs that use the Trinket."""
        return self._specs

    def add_specs(self, *specs: WowSpec) -> None:
        """Name the Specs that use the Trinket.

        Unlike other spells, this does not attach the Trinket to the Specs yet:
        the Game Version does that for the Trinkets of its current Season only.
        """
        self._specs.extend(specs)
