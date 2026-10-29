"""RaidZone and Bosses for Naxxramas (WoW Forever).

The zone id is the Classic Warcraft Logs one; Forever has none of its own yet (#86).
"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.raid_zone import RaidZone

from .anubrekhan import ANUBREKHAN
from .gluth import GLUTH
from .gothik_the_harvester import GOTHIK_THE_HARVESTER
from .grand_widow_faerlina import GRAND_WIDOW_FAERLINA
from .grobbulus import GROBBULUS
from .heigan_the_unclean import HEIGAN_THE_UNCLEAN
from .instructor_razuvious import INSTRUCTOR_RAZUVIOUS
from .kelthuzad import KELTHUZAD
from .loatheb import LOATHEB
from .maexxna import MAEXXNA
from .noth_the_plaguebringer import NOTH_THE_PLAGUEBRINGER
from .patchwerk import PATCHWERK
from .sapphiron import SAPPHIRON
from .thaddius import THADDIUS
from .the_four_horsemen import THE_FOUR_HORSEMEN


NAXXRAMAS = RaidZone(  # ruff: ignore[non-empty-init-module]
    id=1006,
    name="Naxxramas",
    icon="achievement_dungeon_naxxramas.jpg",
    difficulty=RaidDifficulty.NORMAL,
    bosses=[
        ANUBREKHAN,
        GRAND_WIDOW_FAERLINA,
        MAEXXNA,
        NOTH_THE_PLAGUEBRINGER,
        HEIGAN_THE_UNCLEAN,
        LOATHEB,
        INSTRUCTOR_RAZUVIOUS,
        GOTHIK_THE_HARVESTER,
        THE_FOUR_HORSEMEN,
        PATCHWERK,
        GROBBULUS,
        GLUTH,
        THADDIUS,
        SAPPHIRON,
        KELTHUZAD,
    ],
)
