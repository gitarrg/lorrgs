# IMPORT LOCAL LIBRARIES
from lorgs.models import wow_spell
from lorgs.models.wow_spell import SpellType


BONUS_ID_MYTHIC = "bonus=6646"


class WowItem(wow_spell.WowSpell):
    """BaseClass for (useable) items such as Trinkets, Potions or anything else worth tracking."""

    spell_type: str = SpellType.ITEM
    show: bool = False

    item: int
    """Item ID as seen on wowhead/ingame."""

    ilvl: int = 0
    """Item Level to display in the tooltip."""

    bonus_ids: list[str] = [
        "6646",  # Mythic
        "10356",  # Mythic v2 ?
    ]

    def post_init(self) -> None:
        self.wowhead_data = self._gen_wowhead_data()
        return super().post_init()

    def _gen_wowhead_data(self) -> str:
        parts = []

        if self.item:
            parts.append(f"item={self.item}")
        if self.ilvl > 0:
            parts.append(f"ilvl={self.ilvl}")
        if self.bonus_ids:
            bonus_ids = ":".join(self.bonus_ids)
            parts.append(f"bonus={bonus_ids}")

        return "&".join(parts)
