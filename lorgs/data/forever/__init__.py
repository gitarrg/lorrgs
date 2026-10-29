"""Game data of the WoW Forever Game Version.

Registers the Classes and Specs of the beta and the Classic Raids (no spells yet).
`version.py` builds the Game Data and the Game Version from them.
`lorgs.data` imports this package, so every process serves Forever.
"""

# ruff: file-ignore[unused-import, unsorted-imports]

# Roles
from lorgs.data.forever.roles import *

# Classes
from lorgs.data.forever.classes import *

# Raids
from lorgs.data.expansions import classic

# Game Data
from lorgs.data.forever.version import GAME_DATA as GAME_DATA
from lorgs.data.forever.version import GAME_VERSION as GAME_VERSION
