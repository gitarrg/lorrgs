# IMPORT LOCAL LIBRARIES
from lorgs.data.retail.classes import *
from lorgs.models.dungeon import Dungeon
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Trinkets

ALGETHAR_PUZZLE_BOX = WowTrinket(
    spell_id=383781,
    color="#b34747",
    cooldown=180,
    duration=20,
    name="Algeth'ar Puzzle Box",
    icon="inv_misc_enggizmos_18.jpg",
    item=193701,
)
ALGETHAR_PUZZLE_BOX.add_specs(*AGI_SPECS, *STR_SPECS)


################################################################################

ALGETHAR_ACADEMY = Dungeon(name="Algeth'ar Academy", trinkets=[ALGETHAR_PUZZLE_BOX])
