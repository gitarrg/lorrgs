"""Imperator Averzian (Voidspire)

>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/9hZTAp8gFjJcCaNz?fight=5"
"""

from lorgs.data.classes import *  # noqa: F403
from lorgs.models.raid_boss import RaidBoss


AVERZIAN = RaidBoss(
    id=3176,
    name="Imperator Averzian",
    nick="Averzian",
    icon="inv_120_raid_voidspire_hostgeneral.jpg",
)
boss = AVERZIAN


################################################################################
# Trinkets


################################################################################
# Spells

# Tic Tac Toe spawn
boss.add_cast(
    spell_id=1251361,
    name="Shadow's Advance",
    duration=3,
    color="rgb(165, 61, 217)",
    icon="spell_shadow_antishadow.jpg",
)


# Group soaks
boss.add_cast(
    spell_id=1249265,
    name="Umbral Collapse",
    duration=5.5,
    color="rgb(123, 237, 237)",
    icon="inv_ability_darkrangerhunter_blackarrow.jpg",
)


# knockback
boss.add_cast(
    spell_id=1258880,
    name="Void Fall",
    duration=20,
    color="rgb(74, 53, 232)",
    icon="inv_nullstone_void.jpg",
    show=False,
)

# spikes to dodge
boss.add_cast(
    spell_id=1260712,
    name="Oblivion's Wrath",
    duration=3,
    color="rgb(47, 100, 247)",
    icon="spell_priest_void-blast.jpg",
    show=False,
)



"""
boss.add_cast(
    spell_id=1262036,
    name="Void Rupture",
    duration=2,
    color="rgb(232, 143, 42)",
    icon="ability_creature_cursed_03.jpg",
)

boss.add_cast(
    spell_id=1270949,
    name="Desolation",
    duration=7,
    color="rgb(232, 95, 221)",
    icon="inv_112_raidtrinkets_blobofswirlingvoid_gold.jpg",
)


boss.add_cast(
    spell_id=1249251,
    name="Dark Upheaval",
    duration=3,
    color="rgb(95, 212, 130)",
    icon="ability_priest_voidentropy.jpg",
)

boss.add_cast(
    spell_id=1280015,
    name="Void Marked",
    duration=15,
    color="rgb(50, 150, 255)",
    icon="ability_warlock_improvedsoulleech.jpg",
)

boss.add_cast(
    spell_id=1251583,
    name="March of the Endless",
    duration=10,
    color="rgb(242, 7, 54)",
    icon="ability_creature_cursed_03.jpg",
)
"""



################################################################################
# Phases

