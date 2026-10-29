"""RaidZone and Bosses for Ruins of Ahn'Qiraj (WoW Forever).

The zone id is the Classic Warcraft Logs one; Forever has none of its own yet (#86).
"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.raid_zone import RaidZone

from .ayamiss_the_hunter import AYAMISS_THE_HUNTER
from .buru_the_gorger import BURU_THE_GORGER
from .general_rajaxx import GENERAL_RAJAXX
from .kurinnaxx import KURINNAXX
from .moam import MOAM
from .ossirian_the_unscarred import OSSIRIAN_THE_UNSCARRED


RUINS_OF_AHNQIRAJ = RaidZone(  # ruff: ignore[non-empty-init-module]
    id=1004,
    name="Ruins of Ahn'Qiraj",
    icon="inv_misc_ahnqirajtrinket_03.jpg",
    difficulty=RaidDifficulty.NORMAL,
    bosses=[
        KURINNAXX,
        GENERAL_RAJAXX,
        MOAM,
        BURU_THE_GORGER,
        AYAMISS_THE_HUNTER,
        OSSIRIAN_THE_UNSCARRED,
    ],
)
