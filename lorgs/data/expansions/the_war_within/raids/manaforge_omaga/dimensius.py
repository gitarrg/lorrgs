"""0:


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/PGNkyfmYKn6vHCAB?fight=20"

"""

from lorgs.models.raid_boss import RaidBoss
from lorgs.data.classes import *


DIMENSIUS = RaidBoss(
    id=3135,
    name="Dimensius, the All-Devouring",
    nick="Dimensius",
    icon="inv_112_achievement_raid_dimensius.jpg",
)
boss = DIMENSIUS


################################################################################
# Trinkets


################################################################################
# Spells: P1


boss.add_cast(
    spell_id=1229038,
    name="Devour",
    duration=5,
    color="rgb(237, 26, 65)",
    icon="inv_112_raiddimensius_devour.jpg",
    variations=[
        1233539,  # P3
    ],
)

boss.add_cast(
    spell_id=1230979,
    name="Dark Matter",
    duration=4,
    color="rgb(229, 114, 237)",
    icon="spell_fire_twilightflamestrike.jpg",
)

# boss.add_cast(
#     spell_id=1243690,  # CHECK
#     name="Shattered Space",
#     duration=10,
#     color="rgb(66, 64, 227)",
#     icon="inv_ability_voidweaverpriest_entropicrift.jpg",
# )

# boss.add_cast(
#     spell_id=1243577,  # CHECK
#     name="Reverse Gravity",
#     duration=6,
#     color="rgb(169, 232, 198)",
#     icon="inv_112_raiddimensius_reversegravity.jpg",
#     show=False,
# )

boss.add_cast(
    spell_id=1230087,
    name="Massive Smash",
    duration=4,
    color="rgb(184, 140, 99)",
    icon="inv_cosmicvoid_nova.jpg",
)


################################################################################
# Spells: Artoshion & Pargoth


boss.add_cast(
    spell_id=1238765,
    name="Extinction",
    duration=8.5,
    color="rgb(178, 159, 181)",
    icon="inv_112_raiddimensius_brokenworld.jpg",
)


boss.add_cast(
    spell_id=1239262,
    name="Conqueror's Cross",
    duration=2.5,
    color="rgb(104, 26, 163)",
    icon="spell_holy_prayerofshadowprotection.jpg",
    show=False,
)


boss.add_cast(
    spell_id=1237694,
    name="Mass Ejection",
    duration=4,
    color="rgb(29, 209, 209)",
    icon="inv_cosmicvoid_wave.jpg",
    variations=[
        1237695,  # Stardust Nova
    ],
    show=False,
)

# follow up von Mass Ejection?
# boss.add_cast(  # DEBUFF?
#     spell_id=1237325,  # CHECK
#     name="Gamma Burst",
#     duration=4,
#     color="rgb(207, 209, 92)",
#     icon="inv_112_raiddimensius_gammaburst.jpg",
# )


################################################################################
# Spells: P3

boss.add_cast(
    spell_id=1231716,
    name="Extinguish The Stars",
    duration=10,
    color="rgb(26, 42, 150)",
    icon="inv_ability_voidweaverpriest_entropicrift.jpg",
)

# Dausegene Rings
boss.add_cast(
    spell_id=1234044,
    name="Darkened Sky",
    duration=8,
    color="rgb(222, 168, 75)",
    icon="inv_112_raiddimensius_darkenedsky.jpg",
)

boss.add_cast(
    spell_id=1232973,
    name="Supernova",
    duration=5,
    color="rgb(100, 103, 115)",
    icon="inv_112_raiddimensius_supernova.jpg",
    show=False,
)

# debuff on raid? no boss cast
# boss.add_cast(
#     spell_id=1250055,  # CHECK
#     name="Voidgrasp",
#     duration=8,
#     color="rgb(78, 44, 201)",
#     icon="inv_cosmicvoid_orb.jpg",
# )

boss.add_cast(
    spell_id=1234263,
    name="Cosmic Collapse",
    duration=4,
    color="rgb(184, 140, 99)",
    icon="inv_cosmicvoid_nova.jpg",
)


################################################################################
# Phases

boss.add_phase(name="I1", spell_id=1234898, event_type="cast")  # Event Horizon

boss.add_phase(name="Artoshion", spell_id=1246143, event_type="applybuff", count=1)  # Touch of Oblivion
boss.add_phase(name="Pargoth", spell_id=1246143, event_type="applybuff", count=2)  # Touch of Oblivion

boss.add_phase(name="P3", spell_id=1245292, event_type="applybuff")  # Destabilized
