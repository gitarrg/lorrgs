from lorgs.data.classes import ALL_SPECS, HEAL
from lorgs.models.wow_potion import WowPotion
from lorgs.data.constants import COL_MANA


SILVERMOON_HEALTH_POTION = WowPotion(
    spell_id=1234768,
    color="#e35f5f",
    name="Silvermoon Health Potion",
    icon="inv_12_profession_alchemy_lightpotion_orange.jpg",
    item=241305,
    variations=[
        1262857,  # Potent Healing Potion (flat 50%)
    ],
)
"""Health Pot"""
SILVERMOON_HEALTH_POTION.add_specs(*ALL_SPECS)


LIGHTFUSED_MANA_POTION = WowPotion(
    spell_id=1236648,
    color=COL_MANA,
    name="Lightfused Mana Potion",
    icon="inv_12_profession_alchemy_lightpotion_blue.jpg",
    item=241300,
)
"""Mana Pot"""
LIGHTFUSED_MANA_POTION.add_specs(*HEAL.specs)


LIGHTS_POTENTIAL = WowPotion(
    spell_id=1236616,
    duration=30,
    color="hsl(55 100% 55%)",
    name="Light's Potential",
    icon="inv_12_profession_alchemy_lightpotion_yellow.jpg",
    item=241308,
    variations=[],
)
"""Buff main stat

> Use: Drink to increase your primary stat by 695 for 30 sec.
"""
LIGHTS_POTENTIAL.add_specs(*ALL_SPECS)


POTION_OF_RECKLESSNESS = WowPotion(
    spell_id=1236994,
    duration=30,
    color="hsl(300 60% 40%)",
    name="Potion of Recklessness",
    icon="inv_12_profession_alchemy_voidpotion_red.jpg",
    item=241288,
    variations=[],
)
"""Buff highest secondary stat while losing lowest secondary stat

> Use: Gain 1725 of your highest secondary stat while losing 232 of your lowest secondary stat for 30 sec.
"""
POTION_OF_RECKLESSNESS.add_specs(*ALL_SPECS)



MIDNIGHT_CONSUMABLES = [
    SILVERMOON_HEALTH_POTION,
    LIGHTS_POTENTIAL,
    POTION_OF_RECKLESSNESS,
    LIGHTFUSED_MANA_POTION,
]
