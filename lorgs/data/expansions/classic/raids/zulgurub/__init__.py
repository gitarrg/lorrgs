"""RaidZone and Bosses for Zul'Gurub (WoW Forever).

The zone id is the Classic Warcraft Logs one; Forever has none of its own yet (#86).
"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.raid_zone import RaidZone

from .bloodlord_mandokir import BLOODLORD_MANDOKIR
from .edge_of_madness import EDGE_OF_MADNESS
from .gahzranka import GAHZRANKA
from .hakkar import HAKKAR
from .high_priest_thekal import HIGH_PRIEST_THEKAL
from .high_priest_venoxis import HIGH_PRIEST_VENOXIS
from .high_priestess_arlokk import HIGH_PRIESTESS_ARLOKK
from .high_priestess_jeklik import HIGH_PRIESTESS_JEKLIK
from .high_priestess_marli import HIGH_PRIESTESS_MARLI
from .jindo_the_hexxer import JINDO_THE_HEXXER


ZULGURUB = RaidZone(  # ruff: ignore[non-empty-init-module]
    id=1003,
    name="Zul'Gurub",
    icon="achievement_boss_hakkar.jpg",
    difficulty=RaidDifficulty.NORMAL,
    bosses=[
        HIGH_PRIESTESS_JEKLIK,
        HIGH_PRIEST_VENOXIS,
        HIGH_PRIESTESS_MARLI,
        BLOODLORD_MANDOKIR,
        EDGE_OF_MADNESS,
        HIGH_PRIEST_THEKAL,
        GAHZRANKA,
        HIGH_PRIESTESS_ARLOKK,
        JINDO_THE_HEXXER,
        HAKKAR,
    ],
)
