"""0:


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/DzLQG1Rkp4xtdJgh?fight=16"

"""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.wow_trinket import WowTrinket


LOOMITHAR = RaidBoss(
    id=3131,
    name="Loom'ithar",
    nick="Loom'ithar",
    icon="inv_112_achievement_raid_silkworm.jpg",
)
boss = LOOMITHAR


################################################################################
# Trinkets

LOOMITHARS_LIVING_SILK = WowTrinket(
    spell_id=1232721,
    cooldown=90,
    duration=10,
    name="Loom'ithar's Living Silk",
    icon="inv_112_raidtrinkets_astralspinneret.jpg",
    item=242393,
)
"""Shield on target

> Use: Weave an arcane cocoon around yourself and four nearby allies for 10 sec,
> reducing their damage taken by 75% until 3001672 damage has been prevented.
> 
> If a cocoon expires, it bursts to heal an injured ally for 50% of its remaining power.
> (1 Min, 30 Sec Cooldown)

"""
LOOMITHARS_LIVING_SILK.add_specs(*HEAL.specs)
