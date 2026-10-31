"""RaidZone and Bosses for Mogu'shan Vaults (MoP Classic).

Logs:
    All Reports:
    https://classic.warcraftlogs.com/zone/reports?zone=1050

    Rankings:
    https://classic.warcraftlogs.com/zone/rankings/1050
"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.raid_zone import RaidZone

from .elegon import ELEGON
from .feng import FENG
from .garajal import GARAJAL
from .spirit_kings import SPIRIT_KINGS
from .stone_guard import STONE_GUARD
from .will_of_the_emperor import WILL_OF_THE_EMPEROR


################################################################################
#
#   Tier: 1050 Mogu'shan Vaults
#
################################################################################
MOGUSHAN_VAULTS = RaidZone(
    id=1050,
    name="Mogu'shan Vaults",
    icon="achievement_moguraid_01.jpg",
    difficulty=RaidDifficulty.HEROIC,  # WCL has no higher one
    bosses=[
        STONE_GUARD,
        FENG,
        GARAJAL,
        SPIRIT_KINGS,
        ELEGON,
        WILL_OF_THE_EMPEROR,
    ],
)
