"""RaidZone and Bosses for Blackwing Lair (WoW Forever).

The zone id is the Classic Warcraft Logs one; Forever has none of its own yet (#86).
"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.raid_zone import RaidZone

from .broodlord_lashlayer import BROODLORD_LASHLAYER
from .chromaggus import CHROMAGGUS
from .ebonroc import EBONROC
from .firemaw import FIREMAW
from .flamegor import FLAMEGOR
from .nefarian import NEFARIAN
from .razorgore_the_untamed import RAZORGORE_THE_UNTAMED
from .vaelastrasz_the_corrupt import VAELASTRASZ_THE_CORRUPT


BLACKWING_LAIR = RaidZone(  # ruff: ignore[non-empty-init-module]
    id=1002,
    name="Blackwing Lair",
    icon="achievement_boss_nefarion.jpg",
    difficulty=RaidDifficulty.NORMAL,
    bosses=[
        RAZORGORE_THE_UNTAMED,
        VAELASTRASZ_THE_CORRUPT,
        BROODLORD_LASHLAYER,
        FIREMAW,
        EBONROC,
        FLAMEGOR,
        CHROMAGGUS,
        NEFARIAN,
    ],
)
