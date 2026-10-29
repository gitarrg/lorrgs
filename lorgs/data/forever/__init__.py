"""Game data of the WoW Forever Game Version.

Registers the Classes and Specs of the beta and the Classic Raids (no spells yet).
`lorgs.data` imports this package, so every process serves Forever.
"""

# Game Data
import sys

from lorgs.data.forever.classes import *
from lorgs.data.forever.roles import *
from lorgs.data.forever.season import CURRENT_SEASON as CURRENT_SEASON
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.game_data import GameData
from lorgs.models.game_version import GameVersion


GAME_DATA = GameData.from_package(  # ruff: ignore[non-empty-init-module]
    sys.modules[__name__],
    CURRENT_SEASON,
    difficulties=(RaidDifficulty.NORMAL,),
)


GAME_VERSION = GameVersion(  # ruff: ignore[non-empty-init-module]
    name="forever",
    title="WoW Forever",
    wcl_game_version=99,  # placeholder until #86
    data=GAME_DATA,
    collapse_raids=True,
    has_comp_modes=False,
)
