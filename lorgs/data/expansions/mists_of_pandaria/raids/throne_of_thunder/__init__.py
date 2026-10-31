"""RaidZone and Bosses for Throne of Thunder (MoP Classic).

Logs:
    All Reports:
    https://classic.warcraftlogs.com/zone/reports?zone=1046

    Rankings:
    https://classic.warcraftlogs.com/zone/rankings/1046
"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.raid_zone import RaidZone

from .council import COUNCIL
from .dark_animus import DARK_ANIMUS
from .durumu import DURUMU
from .horridon import HORRIDON
from .iron_qon import IRON_QON
from .ji_kun import JI_KUN
from .jinrokh import JINROKH
from .lei_shen import LEI_SHEN
from .megaera import MEGAERA
from .primordius import PRIMORDIUS
from .ra_den import RA_DEN
from .tortos import TORTOS
from .twins import TWINS


################################################################################
#
#   Tier: 1046 Throne of Thunder
#
################################################################################
THRONE_OF_THUNDER = RaidZone(
    id=1051.3,  # WCL zone is 1046; shifted so the frontend (sorts by id) lists it after Terrace of Endless Spring
    name="Throne of Thunder",
    icon="achievement_raid_thunder_king.jpg",
    difficulty=RaidDifficulty.HEROIC,  # WCL has no higher one
    bosses=[
        JINROKH,
        HORRIDON,
        COUNCIL,
        TORTOS,
        MEGAERA,
        JI_KUN,
        DURUMU,
        PRIMORDIUS,
        DARK_ANIMUS,
        IRON_QON,
        TWINS,
        LEI_SHEN,
        RA_DEN,
    ],
)
