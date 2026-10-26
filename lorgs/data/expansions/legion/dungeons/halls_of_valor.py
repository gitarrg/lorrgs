# IMPORT LOCAL LIBRARIES
from lorgs.data.retail.classes import *
from lorgs.models.dungeon import Dungeon
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Trinkets

HORN_OF_VALOR = WowTrinket(
    spell_id=215956,
    color="#6b6bb3",
    cooldown=120,
    duration=30,
    name="Horn of Valor",
    icon="inv_misc_horn_03.jpg",
    item=133642,
)
HORN_OF_VALOR.add_specs(*ALL_SPECS)


################################################################################

HALLS_OF_VALOR = Dungeon(name="Halls of Valor", trinkets=[HORN_OF_VALOR])
