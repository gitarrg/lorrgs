"""RaidZone and Bosses for Patch 12.1 The Venomous Abyss.

Logs:
    All Reports:
    https://www.warcraftlogs.com/zone/reports?zone=54

    Rankings:
    https://www.warcraftlogs.com/zone/rankings/54

"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone


################################################################################
#
#   Tier: 54 The Venomous Abyss
#
################################################################################
THE_VENOMOUS_ABYSS = RaidZone(
    id=54,
    name="The Venomous Abyss",
    icon="inv_misc_questionmark.jpg",
    bosses=[],
)
