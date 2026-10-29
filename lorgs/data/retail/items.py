"""Define Consumeables/Potions players can use."""

# pylint: disable=line-too-long
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

from lorgs.data.retail.classes import *
from lorgs.models.wow_potion import WowPotion


# generic pots for all specs
WowPotion(
    spell_id=6262,
    cooldown=0,  # no cooldown per se. One per fight use.
    color="#63cf48",
    name="Healthstone",
    icon="warlock_-healthstone.jpg",
    item=5512,
).add_specs(*ALL_SPECS)
