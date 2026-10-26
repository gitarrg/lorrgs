# IMPORT LOCAL LIBRARIES
from lorgs.data.retail.classes import *
from lorgs.models.dungeon import Dungeon
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Trinkets

IRIDEUS_FRAGMENT = WowTrinket(
    spell_id=383941,
    color="#ab9671",
    cooldown=180,
    duration=20,
    name="Irideus Fragment",
    icon="inv_10_dungeonjewelry_titan_trinket_1facefragment_color3.jpg",
    item=193743,
    ilvl=447,
    query=False,
)
IRIDEUS_FRAGMENT.add_specs(*ALL_SPECS)


################################################################################

HALLS_OF_INFUSION = Dungeon(name="Halls of Infusion", trinkets=[IRIDEUS_FRAGMENT])
