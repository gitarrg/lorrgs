# IMPORT LOCAL LIBRARIES
from lorgs.data.retail.classes import *
from lorgs.models.dungeon import Dungeon
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Trinkets

BALEFIRE_BRANCH = WowTrinket(
    spell_id=268998,
    event_type="applybuff",
    color="#8434df",
    cooldown=90,
    name="Balefire Branch",
    icon="inv_staff_26.jpg",
    show=False,
    item=159630,
)
BALEFIRE_BRANCH.add_specs(*INT_SPECS)


################################################################################

WAYCREST_MANOR = Dungeon(name="Waycrest Manor", trinkets=[BALEFIRE_BRANCH])
