"""Endpoints for the Builds of the specs."""

from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs.models import spec_builds
from lorrgs_api.dependencies import GameVersionDep


router = fastapi.APIRouter(tags=["builds"], prefix="/builds")


@router.get("/{spec_slug}")
async def get_spec_builds(
    game_version: GameVersionDep,
    response: fastapi.Response,
    spec_slug: str,
) -> spec_builds.BuildsResult:
    """The Builds of one spec and the settings they were worked out with.

    A spec without Builds (yet) returns an empty list.
    Assign a player's Talents to a Build by their distance (talent nodes whose pick differs, hero and spec talents
    only, without `ignore`) to the `talents` of each Build: the nearest within `max(threshold, assign_reach)`, else "Other".
    Talents of another hero tree, or differing in a `force_new_build` entry, never belong to the same Build.
    """
    spec = game_version.data.get_spec(spec_slug) if game_version.has_talents else None
    if not spec or not spec.role.playable:
        raise fastapi.HTTPException(status_code=404, detail="Not found.")

    response.headers["Cache-Control"] = "max-age=3600"  # worked out once a day
    stored = spec_builds.SpecBuilds.get(game_version=game_version.name, spec_slug=spec_slug)
    if stored:
        result = spec_builds.BuildsResult(**stored.model_dump(include=set(spec_builds.BuildsResult.model_fields)))
    else:
        settings = spec_builds.BuildSettings(
            threshold=spec_builds.START_THRESHOLD,
            ignore=spec.builds_ignore,
            force_new_build=spec.builds_force_new,
        )
        result = spec_builds.BuildsResult(settings=settings)
    return result
