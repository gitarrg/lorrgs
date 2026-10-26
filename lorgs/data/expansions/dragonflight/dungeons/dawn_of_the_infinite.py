# IMPORT LOCAL LIBRARIES
from lorgs.data.retail.classes import *
from lorgs.models.dungeon import Dungeon
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Trinkets

ECHOING_TYRSTONE = WowTrinket(
    spell_id=417939,
    color="#ff8a1d",
    cooldown=120,
    name="Echoing Tyrstone",
    icon="ability_paladin_lightofthemartyr.jpg",
    item=207552,
)
ECHOING_TYRSTONE.add_specs(*HEAL.specs)


MIRROR_OF_FRACTURED_TOMORROWS = WowTrinket(
    spell_id=418527,
    color="#40d1be",
    duration=20,
    cooldown=180,
    name="Mirror of Fractured Tomorrows",
    icon="achievement_dungeon_ulduarraid_misc_06.jpg",
    item=207581,
)
MIRROR_OF_FRACTURED_TOMORROWS.add_specs(*DPS_SPECS)


IRIDAL_THE_EARTHS_MASTER = WowTrinket(
    spell_id=419278,
    color="#e7c21f",
    cooldown=180,
    name="Iridal, the Earth's Master",
    icon="inv_staff_2h_dracthyr_c_01.jpg",
    item=208321,
)
IRIDAL_THE_EARTHS_MASTER.add_specs(*INT_SPECS)


################################################################################

DAWN_OF_THE_INFINITE = Dungeon(
    name="Dawn of the Infinite",
    trinkets=[
        ECHOING_TYRSTONE,
        MIRROR_OF_FRACTURED_TOMORROWS,
        IRIDAL_THE_EARTHS_MASTER,
    ],
)
