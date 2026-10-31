"""01: Gnarlroot."""

from lorgs.models.raid_boss import RaidBoss


SMOLDERON = RaidBoss(
    id=2824,
    name="Smolderon",
    icon="inv_achievement_raidemeralddream_smolderon.jpg",
)
boss = SMOLDERON


################################################################################
# Main Phase
#

# Breand of Damnation = Tank Soak + Heal Absorb
boss.add_cast(
    spell_id=421343,
    name="Brand of Damnation",
    duration=3,
    color="hsl(270, 80%, 70%)",
    icon="inv_knife_1h_firelandsraid_d_01.jpg",
)

# Searing Aftermath = Tank Explo with Falloff


# Overheated = Spread + Waves
boss.add_cast(
    spell_id=421455,
    name="Overheated",
    duration=10,
    color="hsl(0, 50%, 50%)",
    icon="ability_warlock_inferno.jpg",
)


# Lava Geysers = AoE + fire puddles
# https://www.wowhead.com/ptr-2/spell=422691/lava-geysers


################################################################################
# Intermission
#
boss.add_cast(
    spell_id=422172,
    name="World In Flames",
    duration=30,
    color="hsl(120, 50%, 50%)",
    icon="ability_racial_foregedinflames.jpg",
)
