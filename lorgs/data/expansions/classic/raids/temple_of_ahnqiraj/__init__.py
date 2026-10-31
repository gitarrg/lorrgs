"""RaidZone and Bosses for Temple of Ahn'Qiraj (WoW Forever).

The zone id is the Classic Warcraft Logs one; Forever has none of its own yet (#86).
"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.raid_zone import RaidZone

from .battleguard_sartura import BATTLEGUARD_SARTURA
from .cthun import CTHUN
from .fankriss_the_unyielding import FANKRISS_THE_UNYIELDING
from .ouro import OURO
from .princess_huhuran import PRINCESS_HUHURAN
from .silithid_royalty import SILITHID_ROYALTY
from .the_prophet_skeram import THE_PROPHET_SKERAM
from .twin_emperors import TWIN_EMPERORS
from .viscidus import VISCIDUS


TEMPLE_OF_AHNQIRAJ = RaidZone(
    id=1005,
    name="Temple of Ahn'Qiraj",
    icon="achievement_boss_cthun.jpg",
    difficulty=RaidDifficulty.NORMAL,
    bosses=[
        THE_PROPHET_SKERAM,
        SILITHID_ROYALTY,
        BATTLEGUARD_SARTURA,
        FANKRISS_THE_UNYIELDING,
        VISCIDUS,
        PRINCESS_HUHURAN,
        TWIN_EMPERORS,
        OURO,
        CTHUN,
    ],
)
