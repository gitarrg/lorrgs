"""03: The Forgotten Experiments."""

from lorgs.models.raid_boss import RaidBoss


FORGOTTEN_EXPERIMENTS = RaidBoss(
    id=2693,
    name="The Forgotten Experiments",
    icon="inv_achievement_raiddragon_forgottenexperiments.jpg",
)
boss = FORGOTTEN_EXPERIMENTS

################################################################################
# shared
#
# tank = stacking dot --> aoe on remove


################################################################################
# Neldirs
#

# frontal: Massive Slam (407733)

# charge
boss.add_cast(
    spell_id=406358,
    name="Rending Charge",
    duration=5,
    color="#eb3f3f",
    icon="ability_xavius_tormentingswipe.jpg",
)

# aoe roar
boss.add_cast(
    spell_id=404713,
    name="Bellowing Roar",
    duration=4,
    color="#7a50b5",
    icon="ability_evoker_oppressingroar.jpg",
)


################################################################################
# Thaldrion
#

# Volatile Spew (405492) --> dodge puddles on ground

# applies debuff --> leaves zone on dispell
boss.add_cast(
    spell_id=405042,
    name="Unstable Essence",
    duration=3,  # --> infite duration?
    color="#3ec9de",
    icon="ability_socererking_arcanemines.jpg",
    show=False,
)

# Raid Wide AOE on 100% energy
boss.add_cast(
    spell_id=407775,
    name="Violent Eruption",
    duration=3,
    color="#eb3f3f",
    icon="spell_shadow_unstableaffliction_3_purple.jpg",
)


################################################################################
# Ryan
#

# push back golden orbs --> shield on boss if they reach him
boss.add_cast(
    spell_id=407552,
    name="Temporal Anomaly",
    duration=2,
    color="#e8bf46",
    icon="ability_evoker_temporalanomaly.jpg",
    show=False,
)

# small circle on few players --> spread

# 100% energy --> deep breath across the room
boss.add_cast(
    spell_id=406227,
    name="Deep Breath",
    duration=3 + 3,  # 2x 3sec casts back to back
    color="#eb3f3f",
    icon="ability_evoker_deepbreath.jpg",
)
