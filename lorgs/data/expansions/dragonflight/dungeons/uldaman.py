# IMPORT LOCAL LIBRARIES
from lorgs.data.retail.classes import *
from lorgs.models.dungeon import Dungeon
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Trinkets

TIME_BREACHING_TALON = WowTrinket(
    spell_id=385884,
    color="#cca633",
    cooldown=150,
    duration=20,  # 20sec buff + 20sec debuff
    name="Time-Breaching Talon",
    icon="inv_10_dungeonjewelry_explorer_trinket_3_color3.jpg",
    item=193791,
)
TIME_BREACHING_TALON.add_specs(*INT_SPECS)


################################################################################

ULDAMAN = Dungeon(name="Uldaman: Legacy of Tyr", trinkets=[TIME_BREACHING_TALON])
