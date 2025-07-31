"""02: Soulbinder Naazindhri


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/DzLQG1Rkp4xtdJgh?fight=16"

"""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.wow_trinket import WowTrinket


NAAZINDHRI = RaidBoss(
    id=3130,
    name="Soulbinder Naazindhri",
    nick="Naazindhri",
    icon="inv_112_achievement_raid_binder.jpg",
)
boss = NAAZINDHRI


################################################################################
# Trinkets

SOULBINDERS_EMBRACE = WowTrinket(
    spell_id=1235425,
    cooldown=60,
    duration=20,
    name="Soulbinder's Embrace",
    icon="inv_112_raidtrinkets_manaforge_tanktrinket1.jpg",
    item=242391,
)
"""On-Use DMG + dmg reduce

> Use: Activate the Soulshield to unleash a shockwave dealing 69119 Arcane damage to all nearby enemies and
> reduce your damage taken by 50% for 20 sec or until 2418789 damage has been prevented. (1 Min Cooldown)
"""
SOULBINDERS_EMBRACE.add_specs(*TANK.specs)
