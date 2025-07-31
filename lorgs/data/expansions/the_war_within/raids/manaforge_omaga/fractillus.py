"""0:


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/DzLQG1Rkp4xtdJgh?fight=16"

"""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.wow_trinket import WowTrinket


FRACTILLUS = RaidBoss(
    id=3133,
    name="Fractillus",
    nick="Fractillus",
    icon="inv_112_achievement_raid_glasselemental.jpg",
)
boss = FRACTILLUS


################################################################################
# Trinkets

UNYIELDING_NETHERPRISM = WowTrinket(
    spell_id=1233556,
    duration=20,
    name="Unyielding Netherprism",
    icon="inv_112_raidtrinkets_voidprism.jpg",
    item=242396,
)
"""stacking buff, On use to gain str/agi == Silken Court Trinket 2.0 

> Equip: Your harmful abilities draw focused void through the prism to deal 172768 Cosmic damage split between your target and nearby enemies.
> Damage increased by 30% per enemy struck, up to 150%.
> This effect may occur every 10 sec and accumulates Latent Power within the prism, up to 15 times. (10s cooldown)
> 
> Use: Consume all Latent Power to gain 2088 Strength or Agility per stack for 20 sec. (20 Sec Cooldown)
"""
UNYIELDING_NETHERPRISM.add_specs(*AGI_SPECS)
UNYIELDING_NETHERPRISM.add_specs(*STR_SPECS)
