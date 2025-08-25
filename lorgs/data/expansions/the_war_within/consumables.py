from lorgs.data.classes import *
from lorgs.models.wow_potion import WowPotion


Algari_Healing_Potion = WowPotion(
    spell_id=431416,
    cooldown=300,
    color="#e35f5f",
    name="Health Pot",
    icon="inv_flask_red.jpg",
    item=211880,
    variations=[],
)
"""Health Pot"""
# no longer used. people should use invigorating instead
# Algari_Healing_Potion.add_specs(*ALL_SPECS)


Invigorating_Healing_Potion = WowPotion(
    spell_id=1238009,
    cooldown=300,
    color="#e35f5f",
    name="Health Pot",
    icon="inv_alchemy_70_flask04.jpg",
    item=244839,
    variations=[],  # logs only show 1 spell ID
)
"""Health Pot"""
Invigorating_Healing_Potion.add_specs(*ALL_SPECS)


Tempered_Potion = WowPotion(
    spell_id=431932,  # Tempered Potion
    duration=30,
    color="#ffe714",
    name="Tempered Potion",
    icon="trade_alchemy_potiona4.jpg",
    item=212265,
    variations=[],
)
"""Buff based on active Flask

> Use: Gain the effects of all inactive Tempered Flasks, increasing their associated secondary stats by 2617 for 30 sec.
"""
Tempered_Potion.add_specs(*ALL_SPECS)


Algari_Mana_Potion = WowPotion(
    spell_id=431418,
    color=COL_MANA,
    name="Algari Mana Potion",
    icon="inv_flask_blue.jpg",
    item=212241,
)
"""Mana Pot"""
Algari_Mana_Potion.add_specs(*HEAL.specs)


TWW_CONSUMABLES = [
    Algari_Healing_Potion,
    Tempered_Potion,
    Algari_Mana_Potion,
]
