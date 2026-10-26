"""RaidZone and Bosses for Siege of Orgrimmar (MoP Classic).

Logs:
    All Reports:
    https://classic.warcraftlogs.com/zone/reports?zone=1054

    Rankings:
    https://classic.warcraftlogs.com/zone/rankings/1054
"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.raid_zone import RaidZone

from .blackfuse import BLACKFUSE
from .dark_shaman import DARK_SHAMAN
from .fallen_protectors import FALLEN_PROTECTORS
from .galakras import GALAKRAS
from .garrosh import GARROSH
from .immerseus import IMMERSEUS
from .juggernaut import JUGGERNAUT
from .klaxxi import KLAXXI
from .malkorok import MALKOROK
from .nazgrim import NAZGRIM
from .norushen import NORUSHEN
from .sha_of_pride import SHA_OF_PRIDE
from .spoils import SPOILS
from .thok import THOK


################################################################################
#
#   Tier: 1054 Siege of Orgrimmar
#
################################################################################
SIEGE_OF_ORGRIMMAR = RaidZone(  # ruff: ignore[non-empty-init-module]
    id=1054,
    name="Siege of Orgrimmar",
    icon="achievement_raid_soo_orgrimmar_outdoors.jpg",
    difficulty=RaidDifficulty.HEROIC,  # WCL has no higher one
    bosses=[
        IMMERSEUS,
        FALLEN_PROTECTORS,
        NORUSHEN,
        SHA_OF_PRIDE,
        GALAKRAS,
        JUGGERNAUT,
        DARK_SHAMAN,
        NAZGRIM,
        MALKOROK,
        SPOILS,
        THOK,
        BLACKFUSE,
        KLAXXI,
        GARROSH,
    ],
)
