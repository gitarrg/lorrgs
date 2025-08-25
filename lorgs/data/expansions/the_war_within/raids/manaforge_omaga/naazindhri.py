"""03: Soulbinder Naazindhri


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/AvbNVBmyrKPDCT4L?fight=17"

"""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss


NAAZINDHRI = RaidBoss(
    id=3130,
    name="Soulbinder Naazindhri",
    nick="Naazindhri",
    icon="inv_112_achievement_raid_binder.jpg",
)
boss = NAAZINDHRI


################################################################################
# Trinkets

SOULBINDERS_EMBRACE = boss.add_trinket(
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


# new cages spawn
boss.add_cast(
    spell_id=1225582,
    name="Soul Calling",
    duration=3,
    color="rgb(160, 76, 245)",
    icon="ability_racial_etherealconnection.jpg",
)


# Break Cage Debuffs #1
boss.add_cast(
    spell_id=1225616,
    name="Soulfire Convergence",
    duration=8,
    color="rgb(122, 216, 235)",
    icon="ability_socererking_arcanereplication_nightborne.jpg",
)


# Break Cage Debuffs #2
boss.add_cast(
    spell_id=1227276,
    name="Soulfray Annihilation",
    duration=6,
    color="rgb(237, 100, 230)",
    icon="spell_arcane_arcane03.jpg",
)


# "Arcane Expulsion" = Knockback + drop stuff
boss.add_cast(
    spell_id=1242088,
    name="Arcane Expulsion",
    duration=4,
    cooldown=15,
    color="rgb(227, 39, 111)",
    icon="spell_nature_astralrecalgroup.jpg",
)


boss.add_cast(
    spell_id=1241100,
    name="Mystic Lash",
    duration=4,
    # cooldown=15, # todo
    color="rgb(201, 162, 113)",
    icon="spell_arcane_arcane01_nightborne.jpg",
    show=False,
)


################################################################################
# Phases
# boss.add_phase(name="P{count}", spell_id=1225582, event_type="cast")
