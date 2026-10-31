"""RaidZone and Bosses for Terrace of Endless Spring (MoP Classic).

Logs:
    All Reports:
    https://classic.warcraftlogs.com/zone/reports?zone=1051

    Rankings:
    https://classic.warcraftlogs.com/zone/rankings/1051
"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.raid_zone import RaidZone

from .lei_shi import LEI_SHI
from .protectors import PROTECTORS
from .sha_of_fear import SHA_OF_FEAR
from .tsulong import TSULONG


################################################################################
#
#   Tier: 1051 Terrace of Endless Spring
#
################################################################################
TERRACE_OF_ENDLESS_SPRING = RaidZone(
    id=1051.2,
    name="Terrace of Endless Spring",
    icon="achievement_raid_terraceofendlessspring04.jpg",
    difficulty=RaidDifficulty.HEROIC,  # WCL has no higher one
    bosses=[
        PROTECTORS,
        TSULONG,
        LEI_SHI,
        SHA_OF_FEAR,
    ],
)
