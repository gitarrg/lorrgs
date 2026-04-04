"""L'ura (March on Qual'danas)"""

from lorgs.data.classes import *  # noqa: F403
from lorgs.models.raid_boss import RaidBoss


LURA = RaidBoss(
    id=3183,
    name="L'ura",
    nick="L'ura",
    icon="inv_120_raid_marchonqueldanas_lura.jpg",
    phase_type=RaidBoss.PhaseType.DYNAMIC,
)
boss = LURA


################################################################################
# Trinkets


################################################################################
# Spells


# Phase 1

# boss.add_cast(
#     spell_id=1244412,
#     name="Death's Dirge",
#     duration=3.5,
#     color="rgb(199, 106, 48)",
#     icon="inv_120_raid_marchonqueldanas_lura.jpg",
# )


boss.add_cast(
    spell_id=1249609,
    name="Dark Rune",
    duration=11.5,
    color="rgb(204, 159, 61)",
    icon="inv_10_inscription_vantusrune_color1.jpg",
)


boss.add_cast(
    spell_id=1253915,
    name="Heaven's Glaives",
    duration=3,
    color="rgb(127, 48, 217)",
    show=False,
    icon="inv_glaive_1h_darknaaru_d_01.jpg",
)


boss.add_cast(
    spell_id=1251386,
    name="Safeguard Prism",
    duration=4,
    color="rgb(45, 204, 95)",
    icon="ability_priest_cascade_shadow.jpg",
)


boss.add_cast(
    spell_id=1267049,
    name="Heaven's Lance",
    duration=2.5,
    color="rgb(173, 157, 132)",
    icon="inv_chest_armor_voidelf_d_01.jpg",
    show=False,
)


# --- Intermission ---

boss.add_cast(
    spell_id=1285563,
    name="Total Eclipse",
    duration=30,
    color="rgb(179, 43, 113)",
    icon="inv12_ability_druid_totaleclipse.jpg",
)


# Phase 2

boss.add_cast(
    spell_id=1282043,
    name="Into the Darkwell",
    duration=6,
    color="rgb(252, 131, 198)",
    icon="inv_112_raidtrinkets_blobofswirlingvoid_purple.jpg",
)


boss.add_cast(
    spell_id=1284525,
    name="Galvanize",
    duration=6,
    color="rgb(158, 207, 219)",
    icon="ability_vehicle_electrocharge.jpg",
)


boss.add_cast(
    spell_id=1282412,
    name="Core Harvest",
    duration=3,
    color="rgb(22, 156, 115)",
    icon="inv_112_raiddimensius_crushinggravity.jpg",
)


# boss.add_cast(
#     spell_id=1281123,
#     name="Dark Meltdown",
#     duration=8,
#     color="rgb(103, 68, 242)",
#     icon="inv_112_raiddimensius_blackhole.jpg",
# )


# --- Phase 3 ---

# boss.add_cast(
#     spell_id=1251343,
#     name="The Dark Archangel",
#     duration=6,
#     color="rgb(227, 39, 79)",
#     icon="ability_priest_darkarchangel.jpg",
# )

# boss.add_cast(
#     spell_id=1263253,
#     name="Black Tide",
#     duration=6,
#     color="rgb(42, 19, 125)",
#     icon="inv_cosmicvoid_wave.jpg",
# )
# 
# boss.add_cast(
#     spell_id=1266388,
#     name="Dark Constellation",
#     duration=5,
#     color="rgb(88, 215, 237)",
#     icon="inv_12_dh_void_ability_starfragments.jpg",
# )
# 
# boss.add_cast(
#     spell_id=1266897,
#     name="Light Siphon",
#     duration=22,
#     color="rgb(176, 119, 230)",
#     icon="inv_112_raiddimensius_devour.jpg",
# )


################################################################################
# Phases
