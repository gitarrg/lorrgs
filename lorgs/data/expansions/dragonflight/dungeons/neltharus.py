# IMPORT LOCAL LIBRARIES
from lorgs.data.retail.classes import *
from lorgs.models.dungeon import Dungeon
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Trinkets

SPOILS_OF_NELTHARUS = WowTrinket(
    spell_id=381768,
    color="#5dcdde",
    cooldown=120,
    duration=20,
    name="Spoils of Neltharus",
    icon="inv_10_dungeonjewelry_dragon_trinket_4_bronze.jpg",
    item=193773,
)
SPOILS_OF_NELTHARUS.add_specs(*INT_DPS_SPECS)


################################################################################

NELTHARUS = Dungeon(name="Neltharus", trinkets=[SPOILS_OF_NELTHARUS])
