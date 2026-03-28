# IMPORT LOCAL LIBRARIES
from lorgs.models import wow_item
from lorgs.models.wow_spell import SpellType


class WowPotion(wow_item.WowItem):
    """Potion or other Consumables with an OnUse-Effect."""

    spell_type: str = SpellType.POTION

    cooldown: int = 300  # default cooldown for all potions


    ilvl: int = 0
    bonus_ids: list[str] = []
