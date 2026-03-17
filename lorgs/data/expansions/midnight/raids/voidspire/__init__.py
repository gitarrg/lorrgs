"""RaidZone and Bosses for Patch 12.0 Voidspire

Bosses:
    https://wago.tools/db2/DungeonEncounter?filter%5BMapID%5D=2912&page=1&sort%5BMapID%5D=desc

Logs:
    All Reports:
    https://www.warcraftlogs.com/zone/reports?zone=46

    Rankings:
    https://www.warcraftlogs.com/zone/rankings/46

"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone
from .averzian import AVERZIAN
from .salhadaar import FALLEN_KING_SALHADAAR
from .lightblinded_vanguard import LIGHTBLINDED_VANGUARD
from .vorasius import VORASIUS
from .vaelgor_ezzorak import VAELGOR_EZZORAK
from .crown_of_the_cosmos import CROWN_OF_THE_COSMOS

################################################################################
#
#   Tier: 46 The Voidspire
#
################################################################################
VOIDSPIRE = RaidZone(
    id=46.1,
    name="The Voidspire",
    icon="inv_achievement_raid_voidspire.jpg",
    bosses=[
        AVERZIAN,
        VORASIUS,
        FALLEN_KING_SALHADAAR,
        VAELGOR_EZZORAK,
        LIGHTBLINDED_VANGUARD,
        CROWN_OF_THE_COSMOS,
    ],
)
