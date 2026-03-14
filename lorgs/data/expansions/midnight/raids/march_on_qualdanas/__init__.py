"""RaidZone and Bosses for Patch 12.0 March on Qual'danas

Bosses:
    https://wago.tools/db2/DungeonEncounter?filter%5BMapID%5D=2913&page=1&sort%5BMapID%5D=desc

Logs:
    All Reports:
    https://www.warcraftlogs.com/zone/reports?zone=46

    Rankings:
    https://www.warcraftlogs.com/zone/rankings/46

"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone

################################################################################
#
#   Tier: 46 March on Qual'danas
#
################################################################################
MARCH_ON_QUALDANAS = RaidZone(
    id=46.3,
    name="March on Qual'danas",
    icon="inv_achievement_raid_riftofaln.jpg",
    bosses=[],
)
