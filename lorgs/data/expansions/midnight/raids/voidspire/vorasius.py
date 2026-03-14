"""Vorasius


>>> PYTHONPATH=. uv run --env-file=.env scripts/load_report.py "https://www.warcraftlogs.com/reports/9hZTAp8gFjJcCaNz?fight=14"

"""

from lorgs.data.classes import *  # noqa: F403
from lorgs.models.raid_boss import RaidBoss


VORASIUS = RaidBoss(
    id=3177,
    name="Vorasius",
    nick="Vorasius",
    icon="inv_120_raid_voidspire_kaiju.jpg",
)
boss = VORASIUS



# slam soak on tank
# fixate adds
# beams


################################################################################
# Trinkets


################################################################################
# Spells

# tank slam (soak)
boss.add_cast(
    spell_id=1241768,
    name="Shadowclaw Slam",
    duration=5,
    color="rgb(232, 143, 42)",
    icon="inv_misc_rylakclaw.jpg",
)

# circles spawned after tank slam
# boss.add_cast(
#     spell_id=1276824,
#     name="Aftershock",
#     duration=2.5,
#     color="rgb(186, 143, 82)",
#     icon="spell_nature_earthquake.jpg",
#     show=False,
# )



# big breath across the room
boss.add_cast(
    spell_id=1256855,
    name="Void Breath",
    duration=15,
    color="rgb(80, 51, 245)",
    icon="inv_cosmicvoid_missile.jpg",
)


boss.add_cast(
    spell_id=1260052,
    name="Primordial Roar",
    duration=5,
    color="rgb(196, 56, 242)",
    icon="spell_fire_twilightflamebreath.jpg",
)


# adds
boss.add_cast(
    spell_id=1254199,
    name="Parasite Expulsion",
    duration=6,
    color="rgb(103, 163, 151)",
    icon="inv_voidcreepermount_blue.jpg",
)

"""
boss.add_cast(
    spell_id=1258967,
    name="Focused Aggression",
    duration=20,
    color="rgb(237, 21, 50)",
    icon="inv_cosmicvoid_missile.jpg",
)


boss.add_cast(
    spell_id=1241686,
    name="Shadowclaw Slam",
    duration=5,
    color="rgb(158, 143, 235)",
    icon="spell_hunter_blackicetrap.jpg",
)
"""


################################################################################
# Phases
