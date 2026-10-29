# IMPORT LOCAL LIBRARIES
from lorgs.models import wow_item
from lorgs.models.wow_spell import SpellType


class WowPotion(wow_item.WowItem):
    """Potion or other Consumables with an OnUse-Effect."""

    spell_type: str = SpellType.POTION

    cooldown: int = 300  # default cooldown for all potions

    roles: list[str] = ["tank", "heal", "mdps", "rdps"]
    """Codes of the Roles that use this potion. A Game Version attaches it to the specs of these Roles."""

    ilvl: int = 0
    bonus_ids: list[str] = []
