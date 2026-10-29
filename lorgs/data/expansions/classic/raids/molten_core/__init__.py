"""RaidZone and Bosses for Molten Core (WoW Forever).

The zone id is the Classic Warcraft Logs one; Forever has none of its own yet (#86).
"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.raid_zone import RaidZone

from .baron_geddon import BARON_GEDDON
from .garr import GARR
from .gehennas import GEHENNAS
from .golemagg_the_incinerator import GOLEMAGG_THE_INCINERATOR
from .lucifron import LUCIFRON
from .magmadar import MAGMADAR
from .majordomo_executus import MAJORDOMO_EXECUTUS
from .ragnaros import RAGNAROS
from .shazzrah import SHAZZRAH
from .sulfuron_harbinger import SULFURON_HARBINGER


MOLTEN_CORE = RaidZone(  # ruff: ignore[non-empty-init-module]
    id=1000,
    name="Molten Core",
    icon="achievement_boss_ragnaros.jpg",
    difficulty=RaidDifficulty.NORMAL,
    bosses=[
        LUCIFRON,
        MAGMADAR,
        GEHENNAS,
        GARR,
        SHAZZRAH,
        BARON_GEDDON,
        SULFURON_HARBINGER,
        GOLEMAGG_THE_INCINERATOR,
        MAJORDOMO_EXECUTUS,
        RAGNAROS,
    ],
)
