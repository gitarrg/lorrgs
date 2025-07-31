"""0:


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/DzLQG1Rkp4xtdJgh?fight=16"

"""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.wow_trinket import WowTrinket


SALHADAAR = RaidBoss(
    id=3134,
    name="Nexus-King Salhadaar",
    nick="Salhadaar",
    icon="inv_112_achievement_raid_salhadaar.jpg",
)
boss = SALHADAAR


################################################################################
# Trinkets

PERFIDIOUS_PROJECTOR = WowTrinket(
    spell_id=0,
    cooldown=120,
    name="Perfidious Projector",
    icon="inv_11_0_etherealraid_communicator_color4.jpg",
    item=242403,
)
"""On use dmg

> Use: Compel an oathbound Shadowguard squad to annihilate your target and nearby enemies,
> dealing 4632871 Cosmic damage split between them.

> Damage increased by 30% per additional enemy, up to 150%. (2 Min Cooldown)
"""
# PERFIDIOUS_PROJECTOR.add_specs(*ALL_SPECS)

# TODO: no "cast".. maybe there is a summon evetn or similar to track this.
