# IMPORT LOCAL LIBRARIES
from lorgs.data.retail.classes import *
from lorgs.models.dungeon import Dungeon
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Trinkets

# [Corrupted Egg Shell]

SKARDYNS_GRACE = WowTrinket(
    spell_id=92099,
    cooldown=120,
    duration=20,
    name="Skardyn's Grace",
    icon="inv_misc_coin_08.jpg",
    item=133282,
)
SKARDYNS_GRACE.add_specs(*AGI_SPECS)


MARK_OF_KHARDROS = WowTrinket(
    spell_id=91374,
    cooldown=90,
    duration=15,
    name="Mark of Khardros",
    icon="inv_hammer_04.jpg",
    item=133300,
)
MARK_OF_KHARDROS.add_specs(*STR_SPECS)


################################################################################

GRIM_BATOL = Dungeon(
    name="Grim Batol",
    trinkets=[
        SKARDYNS_GRACE,
        MARK_OF_KHARDROS,
    ],
)
