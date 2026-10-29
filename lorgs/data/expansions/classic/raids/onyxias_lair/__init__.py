"""RaidZone and Bosses for Onyxia's Lair (WoW Forever).

The zone id is the Classic Warcraft Logs one; Forever has none of its own yet (#86).
"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.raid_zone import RaidZone

from .onyxia import ONYXIA


ONYXIAS_LAIR = RaidZone(  # ruff: ignore[non-empty-init-module]
    id=1001,
    name="Onyxia's Lair",
    icon="achievement_boss_onyxia.jpg",
    difficulty=RaidDifficulty.NORMAL,
    bosses=[
        ONYXIA,
    ],
)
