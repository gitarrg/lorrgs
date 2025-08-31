"""0:


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/pmbqxtTkGAdf9FMK?fight=34"

"""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss


SALHADAAR = RaidBoss(
    id=3134,
    name="Nexus-King Salhadaar",
    nick="Salhadaar",
    icon="inv_112_achievement_raid_salhadaar.jpg",
)
boss = SALHADAAR


################################################################################
# Trinkets

PERFIDIOUS_PROJECTOR = boss.add_trinket(
    spell_id=0,
    cooldown=120,
    name="Perfidious Projector",
    icon="inv_11_0_etherealraid_communicator_color4.jpg",
    item=242403,
)
"""On use dmg

> Use: Compel an oathbound Shadowguard squad to annihilate your target and nearby enemies,
> dealing 4632871 Cosmic damage split between them.

> Damage increased by 30% per additional enemy, up to 150%. (2 Min Cooldown)
"""
# PERFIDIOUS_PROJECTOR.add_specs(*ALL_SPECS)

# TODO: no "cast".. maybe there is a summon evetn or similar to track this.


################################################################################
# Phase 1

# Besiege
# boss.add_cast(
#     spell_id=1227384,
#     name="Fel Rush",
#     duration=23,  # todo: check what duration to display
#     color="rgb(74, 135, 232)",
#     icon="inv_cosmicvoid_missile.jpg",
# )

boss.add_cast(
    spell_id=1224864,
    name="Behead",
    duration=24,
    color="rgb(71, 29, 209)",
    icon="ability_evoker_azurestrike.jpg",
)

boss.add_cast(
    spell_id=1227549,
    name="Banishment",
    duration=8,
    color="rgb(108, 21, 138)",
    icon="spell_nzinsanity_chasedbyshadows.jpg",
)

# Subjue Rule = Tank Combo
boss.add_cast(
    spell_id=1224787,
    name="Conquer",
    duration=4,
    color="rgb(231, 37, 107)",
    icon="inv_legendary_mace.jpg",
)
boss.add_cast(
    spell_id=1224812,
    name="Vanquish",
    duration=2.5,
    color="rgb(103, 74, 195)",
    icon="ability_warrior_decisivestrike.jpg",
)


################################################################################
# Phase 2

boss.add_cast(
    spell_id=1227734,
    name="Coalesce Voidwing",
    duration=6.2,
    color="rgb(240, 225, 91)",
    icon="ability_dragonriding_evasivemaneuvers01.jpg",
)


boss.add_cast(
    spell_id=1228115,
    name="Netherbreaker",
    duration=7,
    color="rgb(235, 30, 136)",
    icon="inv_mace_1h_gryphonrider_d_02_bronze.jpg",
)


boss.add_cast(
    spell_id=1228163,
    name="Dimension Breath",
    duration=4,
    color="rgb(150, 100, 232)",
    icon="ability_priest_cascade_shadow.jpg",
)


# Tank Hit
boss.add_cast(
    spell_id=1234529,
    name="Cosmic Maw",
    duration=1.25,
    color="rgb(209, 170, 128)",
    icon="spell_priest_psyfiend.jpg",
    show=False,
)


################################################################################
# Intermission 1

boss.add_cast(
    spell_id=1228075,
    name="Nexus Beams",
    duration=7,
    color="rgb(80, 237, 242)",
    icon="inv_cosmicvoid_beam.jpg",
)


boss.add_cast(
    spell_id=1230263,
    name="Netherblast",
    duration=3,
    color="rgb(245, 122, 231)",
    icon="spell_fire_twilightpyroblast.jpg",
)


boss.add_cast(
    spell_id=1232399,
    name="Dread Mortar",
    duration=4.5,
    color="rgb(195, 187, 237)",
    icon="ability_druid_cresentburn.jpg",
)


boss.add_cast(
    spell_id=1228053,
    name="Reap",
    duration=1,
    color="rgb(227, 141, 98)",
    icon="ability_mount_voidelfstridermount.jpg",
    show=False,
)


################################################################################
# Intermission 2

boss.add_buff(
    spell_id=1228265,
    name="King's Hunger",
    color="rgb(40, 233, 81)",
    icon="spell_holy_consumemagic.jpg",
)


################################################################################
# Phase 3

boss.add_cast(
    spell_id=1226648,
    name="Galactic Smash",
    duration=4,  # TODO: check duration
    color="rgb(31, 79, 237)",
    icon="artifactability_balancedruid_moonandstars.jpg",
)

# Starkiller Swing
boss.add_cast(
    spell_id=1226024,
    name="Starkiller Swing",
    duration=6,
    color="rgb(206, 225, 242)",
    icon="spell_mage_supernova.jpg",
)

# World in Twilight (1249234) = enrage

################################################################################
# Phases

boss.add_phase(name="P2", spell_id=1227734, event_type="cast")
boss.add_phase(name="I1", spell_id=1228065, event_type="cast")  # Rally the Shadowguard
boss.add_phase(name="I2", spell_id=1228265, event_type="cast")  # King's Hunger
boss.add_phase(name="P3", spell_id=1224822, event_type="cast")  # Tyranny
