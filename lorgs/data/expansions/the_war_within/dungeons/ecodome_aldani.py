# IMPORT LOCAL LIBRARIES
from lorgs.data.classes import *
from lorgs.models.dungeon import Dungeon
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Trinkets


LILY_OF_THE_ETERNAL_WEAVE = WowTrinket(
    spell_id=1244029,
    name="Lily of the Eternal Weave",
    icon="inv_herb_karesh.jpg",
    cooldown=90,
    duration=15,
    item=242494,
)
"""Mastery

> Use: Borrow from the fates of those around you, increasing your Mastery by 2901 for 15 sec.
> (1 Min, 30 Sec Cooldown)
"""
LILY_OF_THE_ETERNAL_WEAVE.add_specs(*INT_SPECS)
LILY_OF_THE_ETERNAL_WEAVE.add_specs(*AGI_SPECS)


################################################################################

ECODOME_ALDANI = Dungeon(
    name="Eco-Dome Al'dani",
    trinkets=[
        LILY_OF_THE_ETERNAL_WEAVE,
    ],
)
