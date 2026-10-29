"""API-Routes to list the Game Versions."""

from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs.data import GAME_VERSIONS


router = fastapi.APIRouter(tags=["game_versions"], prefix="/game_versions")


@router.get("")
async def get_game_versions() -> list[dict]:
    """List all Game Versions.

    Returns:
        list[dict]: the Game Versions (the frontend's settings per Game Version included).
        `wcl_game_version` is the Warcraft Logs id a User Report's `game_version` refers to.

    """
    return [
        {
            "name": version.name,
            "title": version.title,
            "wcl_game_version": version.wcl_game_version,
            "collapse_raids": version.collapse_raids,
            "has_comp_modes": version.has_comp_modes,
        }
        for version in GAME_VERSIONS.values()
    ]
