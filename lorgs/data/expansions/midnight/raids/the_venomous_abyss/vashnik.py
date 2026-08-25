"""Vashnik the Malignant (The Venomous Abyss).

PTR: NS 0.3% wipe
https://www.warcraftlogs.com/reports/pfkrcn7xPdDL1jqH?fight=31

"""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss


VASHNIK = RaidBoss(
    id=3455,
    name="Vashnik the Malignant",
    nick="Vashnik",
    icon="inv_121_raid_achievement_alchemist.jpg",
    phase_type=RaidBoss.PhaseType.DYNAMIC,
)
boss = VASHNIK


################################################################################
# Trinkets


################################################################################
# Spells


# orb spawn
boss.add_cast(
    spell_id=1282516,
    name="Malignant Catalyst",
    duration=5,
    color="rgb(130, 135, 80)",
    icon="inv_ability_poison_groundstate.jpg",
)


# Intermission
boss.add_cast(
    spell_id=1284663,
    name="Imbibe",
    duration=4,
    color="rgb(227, 18, 91)",
    icon="spell_nature_poisoncleansingtotem.jpg",
)

# Tank hit
boss.add_cast(
    spell_id=1280935,
    name="Dripping Fangs",
    duration=2,
    color="rgb(168, 146, 118)",
    icon="ability_creature_poison_01.jpg",
    show=False,
)
