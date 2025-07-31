"""03: Soulbinder Naazindhri


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/AvbNVBmyrKPDCT4L?fight=17"

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


################################################################################
# Spells


# Orbs
boss.add_cast(
    spell_id=1227276,
    name="Soulfray Annihilation",
    duration=6,
    color="hsl(30, 60%, 50%)",
    icon="spell_arcane_arcane03.jpg",
)

# TODO: Lines?


# "Arcane Expulsion" = Knockback + drop stuff
boss.add_cast(
    spell_id=1242088,
    name="Arcane Expulsion",
    duration=4,
    cooldown=15,
    color="hsl(0, 60%, 60%)",
    icon="spell_nature_astralrecalgroup.jpg",
)


# new cages spawn
boss.add_cast(
    spell_id=1225582,
    name="Soul Calling",
    duration=3,
    color="hsl(30, 60%, 50%)",
    icon="ability_racial_etherealconnection.jpg",
)


################################################################################
# Phases

boss.add_phase(name="P{count}", spell_id=1225582, event_type="cast")
