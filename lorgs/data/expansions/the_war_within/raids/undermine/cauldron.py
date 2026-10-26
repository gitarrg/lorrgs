"""02: Cauldron of Carnage.

>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/DzLQG1Rkp4xtdJgh?fight=16"

"""

from lorgs.data.retail.classes import *
from lorgs.models.raid_boss import RaidBoss


CAULDRON = RaidBoss(
    id=3010,
    name="Cauldron of Carnage",
    nick="Cauldron",
    icon="inv_11_arenaboss_colossalclash.jpg",
)
boss = CAULDRON


################################################################################
# Trinkets

FLARENDOS_PILOT_LIGHT = boss.add_trinket(
    spell_id=471142,
    cooldown=120,
    duration=15,
    name="Flarendo's Pilot Light",
    icon="inv_111_flarendosflame_gallywix.jpg",
    item=230191,
)
"""On-Use Int for 15sec + dmg after 3 harmful spells

> Use: Reignite the pilot light to gain 6712 Intellect for 15 sec.
> After casting 3 harmful spells, it unleashes a beam dealing 1664237 Fire damage
> to your primary target and 133138.96 damage to up to 5 enemies in its path. (2 Min Cooldown)
"""
FLARENDOS_PILOT_LIGHT.add_specs(*INT_SPECS)


TORQS_BIG_RED_BUTTON = boss.add_trinket(
    spell_id=470286,
    cooldown=120,
    duration=15,
    name="Torq's Big Red Button",
    icon="inv_111_redbutton_bilgewater.jpg",
    item=230190,
)
"""On-use Strength + dmg after 3 harmful spells, increasing on each use.

> Use: Unleash your inner tempest to gain 6712 Strength for 15 sec.
> Your next 3 abilities cause a lightning blast dealing [(299563 * 0.66 0.66 1)]
> Nature damage to your primary target. Damage increased by 100% with each subsequent blast. (2 Min Cooldown)

"""
TORQS_BIG_RED_BUTTON.add_specs(*STR_SPECS)


################################################################################
# Torq

# small adds
# Voltaic Image

# Pools
boss.add_cast(
    spell_id=463900,
    name="Thunderdrum Salvo",
    duration=8,
    color="hsl(170, 75%, 60%)",
    icon="inv_11_arenaboss_thunderdrumsalvo.jpg",
)

# Tank Hit
boss.add_cast(
    spell_id=463798,
    name="Lightning Bash",
    duration=4,  # not sure how long the combo lasts
    color="#478fb3",
    icon="inv_gizmo_supersappercharge.jpg",
    show=False,
)


################################################################################
# Flarendo


# Group Soak
boss.add_cast(
    spell_id=473650,
    name="Scrapbomb",
    duration=10,
    color="hsl(20, 75%, 60%)",
    icon="inv_10_engineering2_boxofbombs_friendly_color1.jpg",
)

# Beam
boss.add_cast(
    spell_id=472233,
    name="Blastburn Roarcannon",
    duration=3.5,
    cooldown=3,
    color="hsl(40, 75%, 60%)",
    icon="spell_shaman_shockinglava.jpg",
)

# Tank hit
boss.add_cast(
    spell_id=1214190,
    name="Eruption Stomp",
    duration=4,
    color="#478fb3",
    icon="inv_gizmo_supersappercharge.jpg",
    show=False,
)

# Spread
# Molten Phlem


################################################################################
# 100% Energy -> (Intermission)

boss.add_buff(
    spell_id=465872,
    name="Colossal Clash",
    duration=20,
    color="hsl(120, 70%, 50%)",
    icon="inv_11_arenaboss_colossalclash.jpg",
)
