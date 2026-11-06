"""RaidZone and Bosses for Onyxia's Lair (WoW Forever).

The ids are the WoW Forever ones on Warcraft Logs (expansion 3001).
"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.raid_zone import RaidZone

from .onyxia import ONYXIA


ONYXIAS_LAIR = RaidZone(
    id=3001,
    name="Onyxia's Lair",
    icon="achievement_boss_onyxia.jpg",
    difficulty=RaidDifficulty.NORMAL,
    bosses=[
        ONYXIA,
    ],
)
