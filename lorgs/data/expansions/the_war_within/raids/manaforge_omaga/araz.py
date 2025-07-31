"""0:


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/DzLQG1Rkp4xtdJgh?fight=16"

"""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.wow_trinket import WowTrinket


ARAZ = RaidBoss(
    id=3132,
    name="Forgeweaver Araz",
    nick="Araz",
    icon="inv_112_achievement_raid_engineer.jpg",
)
boss = ARAZ


################################################################################
# Trinkets

ARAZS_RITUAL_FORGE = WowTrinket(
    spell_id=1232802,
    cooldown=120,
    duration=30,
    name="Araz's Ritual Forge",
    icon="inv_112_raidtrinkets_trinkettechnomancer_ritualengine.jpg",
    item=242402,
)
"""30sec Main Statt, decaying

> Use: Recklessly feed a portion of your essence to the forge, granting you 25742 Primary Stat decaying over 30 sec
> at the cost of 15% of your maximum health. (2 Min Cooldown)

"""
ARAZS_RITUAL_FORGE.add_specs(*ALL_SPECS)
