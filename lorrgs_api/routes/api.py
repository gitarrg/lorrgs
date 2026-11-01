"""Endpoints related to the Backend/API."""

from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorrgs_api.dependencies import get_game_version
from lorrgs_api.routes import (
    api_builds,
    api_comp_rankings,
    api_game_versions,
    api_season,
    api_spec_rankings,
    api_talents,
    api_tasks,
    api_user_reports,
    api_world_data,
    auth,
    debug,
)


router = fastapi.APIRouter()


################################################################################
# Global Routes (no Game Version in the path)
router.include_router(api_game_versions.router)
router.include_router(api_tasks.router)
router.include_router(api_user_reports.router, prefix="/user_reports")
router.include_router(auth.router, prefix="/auth")
router.include_router(debug.router)

################################################################################
# Versioned Routes: `/api/{game_version}/...`
# Included after the global ones, so those win when a path would match both.
versioned_router = fastapi.APIRouter(prefix="/{game_version}", dependencies=[fastapi.Depends(get_game_version)])
versioned_router.include_router(api_builds.router)
versioned_router.include_router(api_comp_rankings.router)
versioned_router.include_router(api_season.router)
versioned_router.include_router(api_spec_rankings.router)
versioned_router.include_router(api_talents.router)
versioned_router.include_router(api_world_data.router)
router.include_router(versioned_router)


@router.get("/")
@router.get("/{path:path}")
def page_not_found():
    raise fastapi.HTTPException(status_code=404, detail="Invalid Route")
