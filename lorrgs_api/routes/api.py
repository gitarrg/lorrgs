"""Endpoints related to the Backend/API."""

from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorrgs_api.routes import (
    api_comp_rankings,
    api_season,
    api_spec_rankings,
    api_tasks,
    api_user_reports,
    api_world_data,
    auth,
    debug,
)


router = fastapi.APIRouter()


################################################################################
# Child Blueprints
router.include_router(api_comp_rankings.router)
router.include_router(api_season.router)
router.include_router(api_spec_rankings.router)
router.include_router(api_tasks.router)
router.include_router(api_user_reports.router, prefix="/user_reports")
router.include_router(api_world_data.router)
router.include_router(auth.router, prefix="/auth")
router.include_router(debug.router)


@router.get("/")
@router.get("/{path:path}")
def page_not_found(path=""):
    return "Invalid Route", 404
