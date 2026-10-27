"""Game data of the WoW Forever Game Version.

Registers the Classes and Specs of the beta (no spells, Raids or Dungeons yet).
The `lorgs.data` package loads this package when Forever is the active Game Version.
"""

# ruff: file-ignore[unused-import, unsorted-imports]

# Classes
from lorgs.data.forever.classes import *

# Seasons
from lorgs.data.forever.season import CURRENT_SEASON
