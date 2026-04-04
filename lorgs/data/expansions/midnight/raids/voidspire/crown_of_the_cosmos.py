"""Crown of the Cosmos (Voidspire)


>>> PYTHONPATH=. uv run --env-file=.env scripts/load_report.py "https://www.warcraftlogs.com/reports/n7Zh4VCL2crjm1RJ?fight=5"


"""

from lorgs.data.classes import *  # noqa: F403
from lorgs.models.raid_boss import RaidBoss


CROWN_OF_THE_COSMOS = RaidBoss(
    id=3181,
    name="Crown of the Cosmos",
    nick="Alleria",
    icon="inv_120_raid_voidspire_alleria.jpg",
    phase_type=RaidBoss.PhaseType.DYNAMIC,
)
boss = CROWN_OF_THE_COSMOS


################################################################################
# Trinkets


################################################################################
# Spells
#
# Spell IDs / phase grouping from TimelineReminders CrownOfTheCosmos.lua (heroic).



# heal absorbs
boss.add_cast(
    spell_id=1233865,
    name="Null Corona",
    duration=10,
    color="rgb(50, 150, 255)",
    icon="inv_cosmicvoid_groundsate.jpg",
)


# aoe
boss.add_cast(
    spell_id=1233819,
    name="Void Expulsion",
    duration=6,
    color="rgb(88, 38, 237)",
    icon="inv_nullstone_void.jpg",
)


# interrupt
boss.add_cast(
    spell_id=1243743,
    name="Interrupting Tremor",
    duration=5,
    color="rgb(189, 143, 194)",
    show=False,
    icon="ability_priest_surgeofdarkness.jpg",
)


# tank hit
boss.add_cast(
    spell_id=1233787,
    name="Dark Hand",
    duration=2,
    color="rgb(185, 56, 194)",
    show=False,
    icon="ability_creature_disease_05.jpg",
)


# boss.add_debuff(
#     spell_id=1233602,
#     name="Silverstrike Arrow",
#     duration=6,
#     color="rgb(101, 134, 153)",
#     icon="inv_ammo_arrow_03.jpg",
# )


boss.add_cast(
    spell_id=1232467,
    name="Grasp of Emptiness",
    duration=8,
    color="rgb(74, 17, 158)",
    icon="inv_shadowelementalmount.jpg",
)


############# Intermission 1 #############

boss.add_cast(
    spell_id=1243981,
    name="Silverstrike Barrage",
    duration=2,
    color="rgb(184, 224, 230)",
    icon="ability_shootwand.jpg",
)


############# Phase 2 #############

# from P1:
# - Void Expulsion (1233819)

# arrows
boss.add_cast(
    spell_id=1237614,
    name="Ranger Captain's Mark",
    duration=6,
    color="rgb(139, 232, 187)",
    icon="spell_holy_hopeandgrace.jpg",
)


# summon add
boss.add_cast(
    spell_id=1237837,
    name="Call of the Void",
    duration=2,
    color="rgb(87, 123, 230)",
    icon="inv_cosmicvoid_debuff.jpg",
)




#### Add Spells
# - Rift Slash = Tank Hit

boss.add_cast(
    spell_id=1246918,
    name="Cosmic Barrier",
    duration=3,
    color="rgb(60, 190, 230)",
    icon="inv_cosmicvoid_buff.jpg",
)


############# Intermission 2 #############

# nothing happens here


############# Phase 3 #############


# circles to break
boss.add_cast(
    spell_id=1239080,
    name="Aspect of the End",
    duration=8,
    color="rgb(235, 28, 59)",
    icon="spell_warlock_demonsoul.jpg",
)


# swap platform
boss.add_cast(
    spell_id=1238843,
    name="Devouring Cosmos",
    duration=4,
    color="rgb(50, 200, 50)",
    icon="inv_cosmicvoid_orb.jpg",
)
