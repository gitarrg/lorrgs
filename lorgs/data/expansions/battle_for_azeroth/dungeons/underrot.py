# IMPORT LOCAL LIBRARIES
from lorgs.data.retail.classes import *
from lorgs.models.dungeon import Dungeon
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Trinkets

VIAL_OF_ANIMATED_BLOOD = WowTrinket(
    spell_id=268836,
    event_type="applybuff",
    cooldown=90,
    duration=18,
    name="Vial of Animated Blood",
    icon="inv_misc_food_legion_leyblood.jpg",
    item=159625,
)
VIAL_OF_ANIMATED_BLOOD.add_specs(*STR_SPECS)


################################################################################

UNDERROT = Dungeon(
    name="The Underrot",
    trinkets=[
        VIAL_OF_ANIMATED_BLOOD,
    ],
)
