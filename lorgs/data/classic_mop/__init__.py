"""Game data of the WoW Classic: Mists of Pandaria Game Version.

Registers the Classes and Specs plus the Raids of the expansion (no spells yet).
The `lorgs.data` package loads this package when Classic MoP is the active Game Version.
"""

# ruff: file-ignore[unused-import, unsorted-imports]

# Classes
from lorgs.data.classic_mop.classes import *

# Raids
from lorgs.data.expansions import mists_of_pandaria

# Seasons
from lorgs.data.classic_mop.season import CURRENT_SEASON
