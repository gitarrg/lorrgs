"""RaidZone and Bosses for Patch 12.0 Sporefall.

Bosses:
    https://wago.tools/db2/DungeonEncounter?filter%5BMapID%5D=1592&page=1&sort%5BMapID%5D=desc

Logs:
    All Reports:
    https://www.warcraftlogs.com/zone/reports?zone=50

    Rankings:
    https://www.warcraftlogs.com/zone/rankings/50

"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone

from .rotmire import ROTMIRE


################################################################################
#
#   Tier: 50 Sporefall
#
################################################################################
SPOREFALL = RaidZone(
    id=50,
    name="Sporefall",
    icon="inv_misc_questionmark.jpg",
    bosses=[
        ROTMIRE,
    ],
)
