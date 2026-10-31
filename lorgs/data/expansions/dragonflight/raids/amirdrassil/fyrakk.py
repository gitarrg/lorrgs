"""01: Gnarlroot."""

from lorgs.models.raid_boss import RaidBoss


FYRAKK = RaidBoss(
    id=2677,
    name="Fyrakk the Blazing",
    nick="Fyrakk",
    icon="inv_achievement_raidemeralddream_fyrakk.jpg",
)
boss = FYRAKK


################################################################################
# Phase 1


# AoE + suck in
boss.add_cast(
    spell_id=417455,
    name="Dream Rend",
    duration=2.43 + 8,
    color="#c53838",
    icon="sha_spell_fire_bluehellfire_nightmare.jpg",
)


# Puddles
boss.add_cast(
    spell_id=419506,
    name="Firestorm",
    duration=2 + 4,
    color="#ffd000",
    icon="spell_shadow_rainoffire.jpg",
)


boss.add_cast(
    spell_id=419123,
    name="Flamefall",
    duration=5,
    color="#a659a6",
    icon="spell_shaman_stormearthfire.jpg",
)


# Frontal / DMG split?
boss.add_cast(
    spell_id=426368,
    name="Darkflame Cleave",
    duration=2,
    color="#2e43ff",
    icon="inv_axe_1h_emeralddreamraid_d_01.jpg",
    show=False,
)


# P1+P2 Tank Hit
boss.add_cast(
    spell_id=417431,
    name="Fyr'alath's Bite",
    duration=2.43,
    color="#478fb3",
    icon="inv_axe_2h_fyrakk_d_01_shadowflame.jpg",
    show=False,
)


################################################################################
# Intermission 1 ' 70%
# - soak orbs

# Shield
boss.add_buff(
    spell_id=421922,  # or 419144?
    name="Corrupt",
    color="#60b336",
    icon="inv_shield_deathwingraid_d_02.jpg",
)


################################################################################
# Phase 2

boss.add_cast(
    spell_id=421455,
    name="Burning Scales",
    duration=10,
    color="#dd4848",
    icon="inv_10_skinning_scales_red.jpg",
)

# Heal small Adds

# Big Breath --> Dodge + kill Adds
# Landing: big DMG


################################################################################
# Phase 3

# Appocalypse Roar = one shot
# pickup seeds to get biggus shildus
boss.add_cast(
    spell_id=422837,
    name="Apocalypse Roar",
    duration=12,
    color="#bf4040",
    icon="inv_misc_head_dragon_red.jpg",
)


# Breath
boss.add_cast(
    spell_id=410223,
    name="Shadowflame Breath",
    duration=3,
    color="#1cfaef",
    icon="inv_fyrakk_dragonbreath.jpg",
)


# P3 Tank Hit
boss.add_cast(
    spell_id=425492,
    name="Infernal Maw",
    duration=1,
    color="#478fb3",
    icon="ability_physical_taunt.jpg",
    show=False,
)
