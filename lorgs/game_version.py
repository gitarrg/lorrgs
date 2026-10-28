"""The Game Version (Retail, Classic, Forever, ...) this deployment serves.

Each deployment serves exactly one Game Version, picked by the `LORRGS_GAME_VERSION`
environment variable (default: `retail`). It is resolved once, at import time.

This module must stay free of game data: it never imports a data package.
"""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import os

# IMPORT LOCAL LIBRARIES
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.game_version import GameVersion


RETAIL = GameVersion(
    name="retail",
    title="Retail",
    wcl_game_version=1,
    difficulties=(
        RaidDifficulty.HEROIC,
        RaidDifficulty.MYTHIC,
    ),
)

FOREVER = GameVersion(
    name="forever",
    title="WoW Forever",
    wcl_game_version=99,  # placeholder until #86
    difficulties=(RaidDifficulty.NORMAL,),
    collapse_raids=True,
    has_comp_modes=False,
)

MISTS = GameVersion(
    name="mists",
    title="Classic: Mists of Pandaria",
    wcl_game_version=6,
    difficulties=(
        RaidDifficulty.HEROIC,
    ),
    collapse_raids=True,
    has_comp_modes=False,
)


GAME_VERSIONS: dict[str, GameVersion] = {}
GAME_VERSIONS[RETAIL.name] = RETAIL
GAME_VERSIONS[MISTS.name] = MISTS
GAME_VERSIONS[FOREVER.name] = FOREVER

current_game_version = os.getenv("LORRGS_GAME_VERSION") or RETAIL.name
ACTIVE = GAME_VERSIONS[current_game_version]
