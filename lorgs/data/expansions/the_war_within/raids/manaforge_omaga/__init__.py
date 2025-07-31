"""RaidZone and Bosses for Patch 11.2 Manaforge Omega, third raid tier of The War Within.

Bosses:
    https://wago.tools/db2/DungeonEncounter?filter%5BMapID%5D=2810&page=1

Logs:
    All Reports:
    https://www.warcraftlogs.com/zone/reports?zone=44

    Rankings:
    https://www.warcraftlogs.com/zone/rankings/44


    PTR Normal Full Clear
    https://www.warcraftlogs.com/reports/nBPbgV9Gafzm8qrN?&fight=1&fight=8&fight=14&fight=26&fight=28&fight=35&fight=52
    >>> scripts/load_report.py --report nBPbgV9Gafzm8qrN --fight 1 8 14 26 28 35 52

"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone
from .araz import ARAZ
from .dimensius import DIMENSIUS
from .fractillus import FRACTILLUS
from .loomithar import LOOMITHAR
from .naazindhri import NAAZINDHRI
from .plexus_sentinel import PLEXUS_SENTINEL
from .salhadaar import SALHADAAR
from .soul_hunters import SOUL_HUNTERS


################################################################################
#
#   Tier: 42 Liberation of Undermine
#
################################################################################
MANAFORGE_OMEGA = RaidZone(
    id=44,
    name="Manaforge Omega",
    icon="inv_112_achievement_raid_manaforgeomega.jpg",
    bosses=[
        PLEXUS_SENTINEL,
        LOOMITHAR,
        NAAZINDHRI,
        ARAZ,
        SOUL_HUNTERS,
        FRACTILLUS,
        SALHADAAR,
        DIMENSIUS,
    ],
)
