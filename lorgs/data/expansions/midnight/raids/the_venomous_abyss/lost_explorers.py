"""The Lost Explorers (The Venomous Abyss).

PTR NS 31%
https://www.warcraftlogs.com/reports/pfkrcn7xPdDL1jqH?fight=11

"""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss


if typing.TYPE_CHECKING:
    from lorgs.clients import wcl
    from lorgs.models.warcraftlogs_fight import Phase


class LostExplorers(RaidBoss):

    id: int = 3497
    name: str = "The Lost Explorers"
    nick: str = "The Lost Turtles"
    icon: str = "inv_121_raid_achievement_tortollans.jpg"
    phase_type: RaidBoss.PhaseType = RaidBoss.PhaseType.DYNAMIC

    def phase_from_transition(self, transition: wcl.PhaseTransition) -> Phase | None:
        # WCL transition IDs are unreliable; auto-enumerate by timestamp order
        transition.id = 0
        return super().phase_from_transition(transition)


LOST_EXPLORERS = LostExplorers()
boss = LOST_EXPLORERS


################################################################################
# Trinkets


################################################################################
# Spells

##################
# Mor'zahi

boss.add_cast(
    spell_id=1297075,
    name="Final Ascension",
    duration=0,
    cooldown=60,
    color="rgb(245, 163, 64)",
    icon="spell_animarevendreth_nova.jpg",
)


##################
# First Mate Nama

boss.add_cast(
    spell_id=1296062,
    name="Shell Spin",
    duration=4,
    color="rgb(179, 194, 112)",
    icon="inv_cape_special_turtleshell_c_02.jpg",
)


##################
# Scrollsage Iku

boss.add_cast(
    spell_id=1296021,
    name="Blink Nova",
    duration=9,
    color="rgb(101, 67, 181)",
    icon="spell_arcane_blink.jpg",
)

boss.add_cast(
    spell_id=1295854,
    name="Shredding Shards",
    duration=3.5,
    color="rgb(184, 171, 201)",
    icon="spell_frost_iceshard.jpg",
    show=False,
)


################################################################################
"""

boss.add_cast(
    spell_id=1296975,
    name="Mor'zahi's Command",
    duration=60,
    color="rgb(245, 163, 64)",
    icon="ICON_PLACEHOLDER",
)

boss.add_cast(
    spell_id=1292104,
    name="Mushroom Toss",
    duration=7,
    color="rgb(177, 107, 227)",
    icon="ICON_PLACEHOLDER",
)

boss.add_cast(
    spell_id=1296249,
    name="Explosive Surprise",
    duration=10,
    color="rgb(247, 44, 17)",
    icon="ICON_PLACEHOLDER",
)

boss.add_cast(
    spell_id=1291933,
    name="Throw Junk",
    duration=3,
    color="rgb(173, 124, 64)",
    icon="ICON_PLACEHOLDER",
)

boss.add_cast(
    spell_id=1296094,
    name="Mighty Thud",
    duration=10,
    color="rgb(227, 189, 143)",
    icon="ICON_PLACEHOLDER",
)

boss.add_cast(
    spell_id=1295891,
    name="Frostfire Volley",
    duration=5,
    color="rgb(237, 181, 28)",
    icon="ICON_PLACEHOLDER",
)

boss.add_cast(
    spell_id=1292779,
    name="Final Ascension",
    duration=20,
    color="rgb(235, 16, 46)",
    icon="ICON_PLACEHOLDER",
)
"""
