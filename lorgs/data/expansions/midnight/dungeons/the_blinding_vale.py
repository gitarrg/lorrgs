# IMPORT LOCAL LIBRARIES
from lorgs.data.retail.classes import *
from lorgs.models.dungeon import Dungeon


################################################################################
# Trinkets

# no on-use trinkets

################################################################################

THE_BLINDING_VALE = Dungeon(
    id=12859,
    name="The Blinding Vale",
    par_time=30 * 60,  # 30:00
    icon="inv_achievement_dungeon_lightbloom.jpg",
)
