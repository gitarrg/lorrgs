# IMPORT LOCAL LIBRARIES
from lorgs.data.retail.classes import *
from lorgs.models.dungeon import Dungeon
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Trinkets

# [High Speaker's Accretion]
# [Overclocked Gear-a-Rang Launcher]

SKARMORAK_SHARD = WowTrinket(
    spell_id=443407,
    cooldown=90,
    duration=15,
    name="Skarmorak Shard",
    icon="inv_arathordungeon_fragment_color2.jpg",
    item=219300,
)
SKARMORAK_SHARD.add_specs(*STR_SPECS)


################################################################################

STONEVAULT = Dungeon(
    name="Stonevault",
    trinkets=[
        SKARMORAK_SHARD,
    ],
)
