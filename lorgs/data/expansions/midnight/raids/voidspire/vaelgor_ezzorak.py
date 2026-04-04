"""Vaelgor & Ezzorak (Voidspire)


>>> PYTHONPATH=. uv run --env-file=.env scripts/load_report.py "https://www.warcraftlogs.com/reports/QCcJTmxyrGdpZNgK?fight=26"


"""

from lorgs.data.classes import INT_SPECS
from lorgs.models.raid_boss import RaidBoss


VAELGOR_EZZORAK = RaidBoss(
    id=3178,
    name="Vaelgor & Ezzorak",
    nick="Vaelgor",
    icon="inv_120_raid_voidspire_dragonduo.jpg",
)
boss = VAELGOR_EZZORAK


################################################################################
# Trinkets

# [Gloom-Spattered Dreadscale]
VAELGORS_FINAL_STARE = boss.add_trinket(
    spell_id=1260459,
    duration=15,
    cooldown=90,
    name="Vaelgor's Final Stare",
    icon="inv_12_trinket_raid_voidspire_int1_voiddragoneye.jpg",
    item=249346,
)
VAELGORS_FINAL_STARE.add_specs(*INT_SPECS)
"""On-Use Mastery

> Use: Seize the eye's draconic power, granting you 1267 Mastery diminishing
> over 15 sec and allowing you to see hidden enemies. (1 Min, 30 Sec Cooldown)
"""

################################################################################
# Spells


# Beam on Tank
boss.add_cast(
    spell_id=1262623,
    name="Nullbeam",
    duration=4,
    color="rgb(122, 17, 250)",
    icon="ability_ironmaidens_convulsiveshadows.jpg",
    show=False,
)

# circle around each player + spawns orbs
boss.add_cast(
    spell_id=1244917,
    name="Void Howl",
    duration=2.5,
    color="rgb(58, 52, 237)",
    icon="inv_cosmicvoid_orb.jpg",
)

# frontal on random player --> needs dispel
boss.add_cast(
    spell_id=1244221,
    name="Dread Breath",
    duration=4,
    color="rgb(234, 68, 252)",
    icon="ability_rogue_envelopingshadows.jpg",
)

# Orb that needs to be soaked (2 groups)
boss.add_cast(
    spell_id=1245391,
    name="Gloom",
    duration=4,
    color="rgb(107, 231, 237)",
    icon="inv_cosmicvoid_nova.jpg",
)

# tank hit
boss.add_cast(
    spell_id=1265131,
    name="Vaelwing",
    duration=1.5,
    color="rgb(100, 123, 140)",
    icon="inv_icon_wing07c.jpg",
    show=False,
)

# tank hit
boss.add_cast(
    spell_id=1245645,
    name="Rakfang",
    duration=1.5,
    color="rgb(142, 112, 145)",
    icon="inv_misc_rubysanctum4.jpg",
    show=False,
)

# Intermission
boss.add_cast(
    spell_id=1248847,
    name="Radiant Barrier",
    duration=25,
    color="rgb(242, 198, 36)",
    icon="spell_holy_blessedresillience.jpg",
)

# Intermission
boss.add_cast(
    spell_id=1249748,
    name="Midnight Flames",
    duration=20,
    color="rgb(245, 56, 91)",
    icon="inv_cosmicdragonmount.jpg",
)


################################################################################
# Phases
