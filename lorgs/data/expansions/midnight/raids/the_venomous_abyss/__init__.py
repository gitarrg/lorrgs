"""RaidZone and Bosses for Patch 12.1 The Venomous Abyss.

Bosses:
    https://wago.tools/db2/DungeonEncounter?filter%5BMapID%5D=3004&page=1&sort%5BOrderIndex%5D=asc

Logs:
    All Reports:
    https://www.warcraftlogs.com/zone/reports?zone=54

    Rankings:
    https://www.warcraftlogs.com/zone/rankings/54

"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone  # ruff: ignore[unsorted-imports]

from .nekzali import NEKZALI
from .entombed_sentinels import ENTOMBED_SENTINELS
from .vashnik import VASHNIK
from .lost_explorers import LOST_EXPLORERS
from .sszorak import SSZORAK
from .twin_fangs import TWIN_FANGS
from .coiled_altar import COILED_ALTAR
from .ulatek import ULATEK


################################################################################
#
#   Tier: 54 The Venomous Abyss
#
################################################################################
THE_VENOMOUS_ABYSS = RaidZone(  # ruff: ignore[non-empty-init-module]
    id=53.1,
    name="The Venomous Abyss",
    icon="8039569.jpg",
    bosses=[
        NEKZALI, # done
        ENTOMBED_SENTINELS,
        VASHNIK,
        LOST_EXPLORERS,
        SSZORAK,
        TWIN_FANGS,
        COILED_ALTAR,
        ULATEK,
    ],
)
