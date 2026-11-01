"""Endpoints dealing with Rankings per Spec."""

from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs.clients import sqs
from lorgs.logger import logger
from lorgs.models import ranking_status, selectors, warcraftlogs_ranking
from lorgs.models.dirty_marker import DirtyMarker
from lorgs.models.raid_zone import AUTO_DIFFICULTY
from lorgs.models.task_payloads import SpecRankingPayload
from lorrgs_api.dependencies import GameVersionDep


router = fastapi.APIRouter(tags=["spec_ranking"], prefix="/spec_ranking")


@router.get("/status")
async def get_spec_ranking_status(game_version: GameVersionDep, response: fastapi.Response):
    """When every Spec Ranking of the current season was last refreshed and since when it is Dirty.

    The same view the Refresh Planner has: S3 `LastModified` and the Dirty markers.
    """
    response.headers["Cache-Control"] = "no-cache"

    payloads = ranking_status.get_ranking_payloads(game_version)
    data = game_version.data
    return [
        {
            "spec_slug": payloads[candidate.key].spec_slug,
            "boss_slug": payloads[candidate.key].boss_slug,
            "difficulty": payloads[candidate.key].difficulty,
            "metric": payloads[candidate.key].metric,
            "is_default_metric": payloads[candidate.key].metric
            == selectors.default_metric(data.get_spec(payloads[candidate.key].spec_slug)),
            "last_refreshed": candidate.last_refreshed,
            "dirty_since": candidate.dirty_since,
        }
        for candidate in ranking_status.get_candidates(game_version, payloads)
    ]


@router.get("/{spec_slug}/{boss_slug}")
async def get_spec_ranking(
    game_version: GameVersionDep,
    spec_slug: str,
    boss_slug: str,
    difficulty: str = AUTO_DIFFICULTY,
    metric: str = "",
):
    """Get the Rankings for a given Spec and Boss."""
    default_metric = selectors.default_metric(game_version.data.get_spec(spec_slug))
    metric = metric or default_metric

    try:
        # Serve the stored json as it is, without parsing and re-encoding it on every request.
        body = warcraftlogs_ranking.SpecRanking.get_raw(
            game_version=game_version.name,
            boss_slug=boss_slug,
            spec_slug=spec_slug,
            difficulty=game_version.data.resolve_difficulty(boss_slug, difficulty),
            metric=metric,
        )
    except KeyError as e:
        raise fastapi.HTTPException(status_code=404, detail="Not found.") from e

    # Counted with CloudWatch Logs Insights (#130). Only cache misses reach the Lambda.
    logger.info(
        f"spec_ranking_view game_version={game_version.name} spec={spec_slug} boss={boss_slug} "
        f"difficulty={difficulty} metric={metric} default_metric={metric == default_metric}"
    )

    # shorter cache timeout for the start of the tier (where frequent changes happen).
    # Set on the returned Response: FastAPI drops headers set on an injected one.
    return fastapi.Response(body, media_type="application/json", headers={"Cache-Control": "max-age=300"})


@router.get("/{spec_slug}/{boss_slug}/info")
async def get_spec_ranking_info(
    game_version: GameVersionDep,
    response: fastapi.Response,
    spec_slug: str,
    boss_slug: str,
    difficulty: str = AUTO_DIFFICULTY,
    metric: str = "",
):
    """Get the Rankings for a given Spec and Boss."""
    metric = metric or selectors.default_metric(game_version.data.get_spec(spec_slug))

    # shorter cache timeout for the start of the tier (where frequent changes happen)
    response.headers["Cache-Control"] = "max-age=300"

    try:
        # Fetch the json directly for performance reasons.
        # this avoids parsing the json into a model just to dump it back to json right away
        data = warcraftlogs_ranking.SpecRanking.get_json(
            game_version=game_version.name,
            boss_slug=boss_slug,
            spec_slug=spec_slug,
            difficulty=game_version.data.resolve_difficulty(boss_slug, difficulty),
            metric=metric,
        )
    except KeyError as e:
        raise fastapi.HTTPException(status_code=404, detail="Not found.") from e

    data.pop("reports", None)
    return data


################################################################################
# Tasks
#


@router.get("/load")
async def spec_ranking_load(
    game_version: GameVersionDep,
    response: fastapi.Response,
    spec_slug="all",
    boss_slug="all",
    difficulty="all",
    metric="all",
    limit: int = 50,
    *,
    clear: bool = False,
):
    """Queue an update for the given specs and bosses."""
    response.headers["Cache-Control"] = "no-cache"

    payload = SpecRankingPayload(
        game_version=game_version.name,
        spec_slug=spec_slug,
        boss_slug=boss_slug,
        difficulty=difficulty,
        metric=metric,
        limit=limit,
        clear=clear,
    )
    message = sqs.send_message(payload=payload)

    return {
        "message": "task queued",
        "task": message.get("MessageId"),
        "payload": payload,
    }


@router.patch("/dirty")
async def flag_dirty(
    game_version: GameVersionDep,
    response: fastapi.Response,
    spec_slug: str,
    boss_slug: str,
    difficulty: str = AUTO_DIFFICULTY,
    metric: str = "",
    *,
    dirty: bool = True,
):
    """Flag a Spec Ranking as dirty."""
    response.headers["Cache-Control"] = "no-cache"

    metric = metric or selectors.default_metric(game_version.data.get_spec(spec_slug))

    marker = DirtyMarker(
        game_version=game_version.name,
        spec_slug=spec_slug,
        boss_slug=boss_slug,
        difficulty=game_version.data.resolve_difficulty(boss_slug, difficulty),
        metric=metric,
    )
    if dirty:
        marker.save()
    else:
        marker.clear()

    return {
        "message": "success",
    }
