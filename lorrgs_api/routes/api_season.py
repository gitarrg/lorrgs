"""API-Routes to fetch Data about seasonal Data."""

from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs.data import CURRENT_SEASON
from lorgs.models.season import Season


router = fastapi.APIRouter(tags=["seasons"], prefix="/seasons")


@router.get("/{season_slug}")
async def get_season(season_slug: str) -> dict:
    """Get a Season.

    Args:
        season_slug (str): Slug of the Season.
            "current" for the current Season

    Returns:
        dict: Season data.

    """
    if season_slug.lower() == "current":
        season = CURRENT_SEASON
    else:
        season = Season.get(slug=season_slug)
        if not season:
            raise fastapi.HTTPException(status_code=404, detail="Invalid Season.")

    return {
        "name": season.name,
        "slug": season.slug,
        "raids": [raid.id for raid in season.raids],
    }
