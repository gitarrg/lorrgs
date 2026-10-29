"""Game data of the WoW Forever Game Version.

Registers the Classes and Specs of the beta (no spells, Raids or Dungeons yet).
The `lorgs.data` package loads this package when Forever is the active Game Version.
"""

from lorgs.data.forever.classes import *
from lorgs.data.forever.roles import *
from lorgs.data.forever.season import CURRENT_SEASON as CURRENT_SEASON

# Game Data
import sys

from lorgs.game_version import FOREVER
from lorgs.models.game_data import GameData

GAME_DATA = GameData.from_package(FOREVER, sys.modules[__name__], CURRENT_SEASON)
FOREVER_GAME_DATA = GAME_DATA
