# IMPORT LOCAL LIBRARIES
from lorgs.data.retail.classes import *
from lorgs.models.dungeon import Dungeon
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Trinkets

MYDAS_TALISMAN = WowTrinket(
    spell_id=265954,
    color="#d3d01a",
    cooldown=90,
    name="My'das Talisman",
    icon="inv_offhand_draenei_a_02.jpg",
    item=158319,
)


################################################################################

ATAL_DAZAR = Dungeon(name="Atal'Dazar", trinkets=[MYDAS_TALISMAN])
