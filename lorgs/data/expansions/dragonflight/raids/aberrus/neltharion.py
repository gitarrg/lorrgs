"""07: Echo of Neltharion."""

from lorgs.models.raid_boss import RaidBoss


NELTHARION = RaidBoss(
    id=2684,
    name="Echo of Neltharion",
    nick="Neltharion",
    icon="inv_achievement_raiddragon_neltharion.jpg",
)
boss = NELTHARION

################################################################################
# Phase 1:
boss.add_cast(
    spell_id=407207,
    name="Rushing Darkness",
    duration=5,
    icon="inv_cosmicvoid_missile.jpg",
    color="#3a79f0",
    show=False,
)


boss.add_cast(
    spell_id=410968,
    name="Volcanic Heart",
    duration=7,
    icon="inv_ragnaros_heart.jpg",
    color="#c94949",
)

boss.add_cast(
    spell_id=403272,
    name="Echoing Fissure",
    duration=5,
    icon="spell_nature_earthquake.jpg",
    color="#bf8143",
)


# Tank:
# Calamious Strike --> big dropoff aoe circle
#
boss.add_cast(
    spell_id=406222,
    name="Calamitous Strike",
    duration=2,
    icon="inv_sword_138.jpg",
    color="#478fb3",
    show=False,
)


################################################################################
# Phase 2
#

# p2 start?
boss.add_cast(
    spell_id=403057,
    name="Surrender to Corruption",
    duration=10,
    icon="inv_cosmicvoid_debuff.jpg",
    color="#60b336",
    show=False,
)


boss.add_cast(
    spell_id=405433,
    name="Umbral Annihilation",
    duration=3,
    icon="inv_cosmicvoid_groundsate.jpg",
    color="#426bd4",
    show=True,
)


# Tank Hit:
# split soul --> use to break walls
boss.add_cast(
    spell_id=407790,
    name="Sunder Shadow",
    duration=1.5 + 5,  # 1.5sec cast + 5sec debuff
    icon="spell_deathknight_spelldeflection.jpg",
    color="#478fb3",
    show=False,
)


################################################################################
# Phase 3
#

boss.add_cast(
    spell_id=407917,
    name="Ebon Destruction",
    duration=6,
    icon="inv_misc_head_dragon_black_nightmare.jpg",
    color="#7b69d6",
    show=True,
)
