"""RaidZone and Bosses for Patch 12.1 The Tidebound Grotto.

Bosses:
    https://wago.tools/db2/DungeonEncounter?filter%5BMapID%5D=2987&page=1

Logs:
    All Reports:
    https://www.warcraftlogs.com/zone/reports?zone=53

    Rankings:
    https://www.warcraftlogs.com/zone/rankings/53

"""
# ruff: file-ignore[non-empty-init-module]

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone

from .nymrissa_wavecaller import NYMRISSA_WAVECALLER


################################################################################
#
#   Tier: 51 The Tidebound Grotto
#
################################################################################
THE_TIDEBOUND_GROTTO = RaidZone(
    id=51.2,
    name="The Tidebound Grotto",
    icon="achievement_boss_elitenagamale.jpg",
    bosses=[
        NYMRISSA_WAVECALLER,
    ],
)
