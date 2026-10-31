"""RaidZone and Bosses for Patch 11.1 Liberation of Undermine, second raid tier of The War Within.

Bosses:
    https://wago.tools/db2/DungeonEncounter?filter[MapID]=exact%3A2769&page=1

Logs:
    All Reports:
    https://www.warcraftlogs.com/zone/reports?zone=42

    Rankings:
    https://www.warcraftlogs.com/zone/rankings/42


    PTR Normal Full Clear
    https://www.warcraftlogs.com/reports/nBPbgV9Gafzm8qrN?&fight=1&fight=8&fight=14&fight=26&fight=28&fight=35&fight=52
    >>> scripts/load_report.py --report nBPbgV9Gafzm8qrN --fight 1 8 14 26 28 35 52

"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone

from .cauldron import CAULDRON
from .gallywix import GALLYWIX
from .lockenstock import LOCKENSTOCK
from .mugzee import MUGZEE
from .one_armed_bandit import ONE_ARMED_BANDIT
from .rik import RIK
from .stix import STIX
from .vexie import VEXIE


################################################################################
#
#   Tier: 42 Liberation of Undermine
#
################################################################################
LIBERATION_OF_UNDERMINE = RaidZone(
    id=42,
    name="Liberation of Undermine",
    icon="inv_achievement_zone_undermine.jpg",
    bosses=[
        VEXIE,
        CAULDRON,
        RIK,
        STIX,
        LOCKENSTOCK,
        ONE_ARMED_BANDIT,
        MUGZEE,
        GALLYWIX,
    ],
)
