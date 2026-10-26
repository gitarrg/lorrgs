# IMPORT LOCAL LIBRARIES
from lorgs.data.retail.classes import *
from lorgs.models.dungeon import Dungeon
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Trinkets

WITHERBARKS_BRANCH = WowTrinket(
    spell_id=429257,
    color="#39d31a",
    cooldown=90,
    name="Witherbark's Branch",
    icon="inv_misc_branch_01.jpg",
    item=109999,
)
WITHERBARKS_BRANCH.add_specs(*AGI_SPECS)


################################################################################

EVERBLOOM = Dungeon(name="Everbloom", trinkets=[WITHERBARKS_BRANCH])
