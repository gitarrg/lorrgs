"""RaidZone and Bosses for Heart of Fear (MoP Classic).

Logs:
    All Reports:
    https://classic.warcraftlogs.com/zone/reports?zone=1051

    Rankings:
    https://classic.warcraftlogs.com/zone/rankings/1051
"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.raid_zone import RaidZone

from .garalon import GARALON
from .meljarak import MELJARAK
from .shekzeer import SHEKZEER
from .tayak import TAYAK
from .unsok import UNSOK
from .zorlok import ZORLOK


################################################################################
#
#   Tier: 1051 Heart of Fear
#
################################################################################
HEART_OF_FEAR = RaidZone(
    id=1051.1,
    name="Heart of Fear",
    icon="achievement_raid_mantidraid01.jpg",
    difficulty=RaidDifficulty.HEROIC,  # WCL has no higher one
    bosses=[
        ZORLOK,
        TAYAK,
        GARALON,
        MELJARAK,
        UNSOK,
        SHEKZEER,
    ],
)
