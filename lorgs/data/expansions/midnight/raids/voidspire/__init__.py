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

################################################################################
#
#   Tier: 46 The Voidspire
#
################################################################################
VOIDSPIRE = RaidZone(
    id=46.1,
    name="The Voidspire",
    icon="inv_achievement_raid_voidspire.jpg",
    bosses=[],
)
