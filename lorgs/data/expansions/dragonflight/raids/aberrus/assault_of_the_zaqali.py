"""04: Assault of the Zaqali."""

from lorgs.models.raid_boss import RaidBoss


ASSAULT_OF_THE_ZAQALI = RaidBoss(
    id=2682,
    name="Assault of the Zaqali",
    icon="inv_achievement_raiddragon_zaqaliassault.jpg",
)
boss = ASSAULT_OF_THE_ZAQALI

# Ignara's Flame (411230) = p0 -> p1 ?
boss.add_buff(
    spell_id=411230,
    name="Ignara's Flame",
    color="#30bf30",
    icon="ability_mage_moltenarmor.jpg",
)

################################################################################
# Phase 1 (adds)
#


# Mystic:
# - spwans with shield --> break asap (pulses aoe while up)
# - dot on random players (dispel)
# - kick lava bolt


# jump --> dodge circle + waves
boss.add_cast(
    spell_id=408959,
    name="Devastating Leap",
    duration=4.3,
    color="#bf8330",
    icon="spell_nature_earthquake.jpg",
)

################################################################################
# Phase 2
#

# 10% Heal
boss.add_buff(
    spell_id=409359,
    name="Desperate Immolation",
    duration=10,
    color="#30bf30",
    icon="spell_nature_unleashedrage.jpg",
)


# grp soak cast
boss.add_cast(
    spell_id=410516,
    name="Catastrophic Slam",
    duration=4.3,
    color="#bf3030",
    icon="ability_earthen_pillar.jpg",
)
