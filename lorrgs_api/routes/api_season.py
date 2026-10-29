"""API-Routes to fetch Data about seasonal Data."""

from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorrgs_api.dependencies import GameVersionDep


router = fastapi.APIRouter(tags=["seasons"], prefix="/seasons")


@router.get("/{season_slug}")
async def get_season(game_version: GameVersionDep, season_slug: str) -> dict:
    """Get a Season.

    Args:
        season_slug (str): Slug of the Season.
            "current" for the current Season

    Returns:
        dict: Season data.

    """
    if season_slug.lower() == "current":
        season = game_version.data.current_season
    else:
        season = game_version.data.get_season(season_slug)
        if not season:
            raise fastapi.HTTPException(status_code=404, detail="Invalid Season.")

    return {
        "name": season.name,
        "slug": season.slug,
        "raids": [raid.id for raid in season.raids],
    }
