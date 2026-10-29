"""Game data of the WoW Classic: Mists of Pandaria Game Version.

Registers the Classes and Specs plus the Raids of the expansion (no spells yet).
`lorgs.data` imports this package, so every process serves Mists.
"""

# ruff: file-ignore[unused-import, unsorted-imports]

# Roles
from lorgs.data.mists.roles import ALL_ROLES

# Classes
from lorgs.data.mists.classes import (
    DEATHKNIGHT,
    DRUID,
    HUNTER,
    MAGE,
    MONK,
    PALADIN,
    PRIEST,
    ROGUE,
    SHAMAN,
    WARLOCK,
    WARRIOR,
)

# Raids
from lorgs.data.expansions import mists_of_pandaria


# Seasons
from lorgs.data.mists.seasons import (
    MISTS_PHASE1,
    MISTS_PHASE2,
    MISTS_PHASE3,
    MISTS_PHASE4,
    MISTS_PHASE5,
)

# Game Data
from lorgs.data.mists.version import (
    GAME_DATA,
    GAME_VERSION,
)
