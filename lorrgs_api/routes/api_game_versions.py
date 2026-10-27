"""API-Routes to list the Game Versions."""

from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs import game_version


router = fastapi.APIRouter(tags=["game_versions"], prefix="/game_versions")


@router.get("")
async def get_game_versions() -> list[dict]:
    """List all Game Versions.

    Each deployment serves a single Game Version (`active`).
    The others are only reachable from the frontend if their `api_url` is configured
    (env `LORRGS_API_URL_<NAME>`).

    Returns:
        list[dict]: the Game Versions (the frontend's settings per Game Version included).

    """
    return [
        {
            "name": version.name,
            "title": version.title,
            "api_url": version.api_url,
            "active": version is game_version.ACTIVE,
            "collapse_raids": version.collapse_raids,
            "has_comp_modes": version.has_comp_modes,
        }
        for version in game_version.GAME_VERSIONS.values()
    ]
