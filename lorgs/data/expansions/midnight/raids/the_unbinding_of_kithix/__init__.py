"""RaidZone and Bosses for Patch 12.1.5 The Unbinding of Kith'ix.

Bosses:
    https://wago.tools/db2/DungeonEncounter?filter%5BMapID%5D=3095&page=1

Logs:
    All Reports:
    https://www.warcraftlogs.com/zone/reports?zone=53

    Rankings:
    https://www.warcraftlogs.com/zone/rankings/53

"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone

from .kithix import KITHIX


################################################################################
#
#   Tier: 53 The Unbinding of Kith'ix
#
################################################################################
THE_UNBINDING_OF_KITHIX = RaidZone(
    id=53.3,
    name="The Unbinding of Kith'ix",
    icon="8214194.jpg",
    bosses=[
        KITHIX,
    ],
)
