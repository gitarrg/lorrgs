"""Game data of the WoW Classic: Mists of Pandaria Game Version.

Registers the Classes and Specs plus the Raids of the expansion (no spells yet).
The `lorgs.data` package loads this package when Mists is the active Game Version.
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

from lorgs.game_version import MISTS
from lorgs.models.game_data import GameData

GAME_DATA = GameData.from_package(MISTS, sys.modules[__name__], CURRENT_SEASON)
MISTS_GAME_DATA = GAME_DATA
