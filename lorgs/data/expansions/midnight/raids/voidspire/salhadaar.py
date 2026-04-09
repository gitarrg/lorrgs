"""Fallen-King Salhadaar (Voidspire)



>>> PYTHONPATH=. uv run --env-file=.env scripts/load_report.py "https://www.warcraftlogs.com/reports/9hZTAp8gFjJcCaNz?fight=21"

"""

from lorgs.data.classes import *  # noqa: F403
from lorgs.models.raid_boss import RaidBoss


FALLEN_KING_SALHADAAR = RaidBoss(
    id=3179,
    name="Fallen-King Salhadaar",
    nick="Salhadaar",
    icon="inv_120_raid_voidspire_salhadaar.jpg",
)
boss = FALLEN_KING_SALHADAAR


# spawn orbs --> kill (raden)
# spawn images --> kick
# debuff on random people -> dispel
# random people = spawn spikes
# 100% energy = big aoe + beams + dmg amp


################################################################################
# Trinkets


# [Wraps of Cosmic Madness]
 

################################################################################
# Spells


# spawn orbs
boss.add_cast(
    spell_id=1247738,
    name="Void Convergence",
    duration=3,
    color="rgb(79, 34, 227)",
    icon="inv_112_raiddimensius_gravity.jpg",
)


# Intermission (big aoe, dmg amp and beams)
boss.add_cast(
    spell_id=1246175,
    name="Entropic Unraveling",
    duration=20,
    color="rgb(247, 17, 63)",
    icon="inv_112_etherealwraps_empowered_blue.jpg",
)


# spikes
boss.add_cast(
    spell_id=1253032,
    name="Shattering Twilight",
    duration=5,
    color="rgb(114, 20, 168)",
    icon="inv_mace_2h_etherealking_d_01.jpg",
)


# images
boss.add_cast(
    spell_id=1254081,
    name="Fractured Projection",
    duration=6,
    color="rgb(234, 138, 237)",
    icon="inv_112_raidtrinkets_netheroverlaymatrix.jpg",
)



# random debuff (heal absorb, needs dispel)
boss.add_cast(
    spell_id=1248697,
    name="Despotic Command",
    duration=14,
    color="rgb(50, 150, 255)",
    icon="inv_cosmicvoid_debuff.jpg",
)


# Random raid dmg
# boss.add_cast(
#     spell_id=1250686,
#     name="Twisting Obscurity",
#     duration=23,
#     color="rgb(230, 110, 41)",
#     icon="inv_cosmicvoid_missile.jpg",
#     show=False,
# )


################################################################################
# Phases
