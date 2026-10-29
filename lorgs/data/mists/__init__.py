"""Game data of the WoW Classic: Mists of Pandaria Game Version.

Registers the Classes and Specs plus the Raids of the expansion (no spells yet).
`lorgs.data` imports this package, so every process serves Mists.
"""

# ruff: file-ignore[unused-import, unsorted-imports]

# Roles
from lorgs.data.mists.roles import *

# Classes
from lorgs.data.mists.classes import *

# Raids
from lorgs.data.expansions import mists_of_pandaria

# Seasons
from lorgs.data.mists.season import CURRENT_SEASON

# Game Data
import sys

from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.game_data import GameData
from lorgs.models.game_version import GameVersion

GAME_DATA = GameData.from_package(sys.modules[__name__], CURRENT_SEASON, difficulties=(RaidDifficulty.HEROIC,))

GAME_VERSION = GameVersion(
    name="mists",
    title="Classic: Mists of Pandaria",
    wcl_game_version=6,
    data=GAME_DATA,
    collapse_raids=True,
    has_comp_modes=False,
)
