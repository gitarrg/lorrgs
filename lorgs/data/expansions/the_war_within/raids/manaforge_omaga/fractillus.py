"""0:


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/B8TZkGKaXQn6rCFA?fight=25"

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


################################################################################
# Spells

# 4x Player Walls
boss.add_cast(
    spell_id=1233416,
    name="Crystalline Shockwave",
    duration=10,
    color="rgb(33, 255, 244)",
    icon="spell_hunter_blackicetrap.jpg",
)

# Tank Wall
boss.add_cast(
    spell_id=1220394,
    name="Shattering Backhand",
    duration=2,
    color="rgb(242, 98, 46)",
    icon="inv_enchant_metamorphiccrystal.jpg",
)

# Wall Break
boss.add_cast(
    spell_id=1231871,
    name="Shockwave Slam",
    duration=4,
    color="rgb(209, 157, 98)",
    icon="inv_leycrystallarge.jpg",
)
