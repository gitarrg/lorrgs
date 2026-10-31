"""RaidZone and Bosses for Patch 11.0 Nerub-ar Palace, first raid tier of The War Within."""

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone

from .ansurek import ANSUREK
from .bloodbound_horror import BLOODBOUND_HORROR
from .kyveza import KYVEZA
from .ovinax import OVINAX
from .rashanan import RASHANAN
from .sikran import SIKRAN
from .silken_court import SILKEN_COURT
from .trinkets import *
from .ulgrax import ULGRAX


################################################################################
#
#   Tier: 38 Nerub-ar Palace
#
################################################################################
NERUBAR_PALACE = RaidZone(
    id=38,
    name="Nerub-ar Palace",
    icon="achievement_zone_azjkahet.jpg",
    bosses=[
        ULGRAX,
        BLOODBOUND_HORROR,
        SIKRAN,
        RASHANAN,
        OVINAX,
        KYVEZA,
        SILKEN_COURT,
        ANSUREK,
    ],
)
