"""Endpoints dealing with Rankings per Spec."""
from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs.clients import sqs
from lorgs.logger import logger
from lorgs.models import warcraftlogs_ranking
from lorgs.models.task_payloads import SpecRankingPayload
from lorgs.models.wow_spec import WowSpec


router = fastapi.APIRouter(tags=["spec_ranking"], prefix="/spec_ranking")


@router.get("/{spec_slug}/{boss_slug}")
async def get_spec_ranking(
    response: fastapi.Response,
    spec_slug: str,
    boss_slug: str,
    difficulty: str = "mythic",
    metric: str = "",
):
    """Get the Rankings for a given Spec and Boss."""
    if not metric:
        spec = WowSpec.get(full_name_slug=spec_slug)
        metric = spec.role.metric if spec else "dps"

    logger.info(f"{spec_slug}/{boss_slug} | start ({difficulty}/{metric})")

    # shorter cache timeout for the start of the tier (where frequent changes happen)
    response.headers["Cache-Control"] = "max-age=300"

    try:
        # Fetch the json directly for performance reasons.
        # this avoids parsing the json into a model just to dump it back to json right away
        return warcraftlogs_ranking.SpecRanking.get_json(
            boss_slug=boss_slug,
            spec_slug=spec_slug,
            difficulty=difficulty,
            metric=metric,
        )
    except KeyError:
        raise fastapi.HTTPException(status_code=404, detail="Not found.")


@router.get("/{spec_slug}/{boss_slug}/info")
async def get_spec_ranking_info(
    response: fastapi.Response,
    spec_slug: str,
    boss_slug: str,
    difficulty: str = "mythic",
    metric: str = "",
):
    """Get the Rankings for a given Spec and Boss."""
    if not metric:
        spec = WowSpec.get(full_name_slug=spec_slug)
        metric = spec.role.metric if spec else "dps"

    # shorter cache timeout for the start of the tier (where frequent changes happen)
    response.headers["Cache-Control"] = "max-age=300"

    try:
        # Fetch the json directly for performance reasons.
        # this avoids parsing the json into a model just to dump it back to json right away
        data = warcraftlogs_ranking.SpecRanking.get_json(
            boss_slug=boss_slug,
            spec_slug=spec_slug,
            difficulty=difficulty,
            metric=metric,
        )
    except KeyError:
        raise fastapi.HTTPException(status_code=404, detail="Not found.")

    data.pop("reports", None)
    return data


################################################################################
# Tasks
#


@router.get("/load")
async def spec_ranking_load(
    response: fastapi.Response,
    spec_slug="all",
    boss_slug="all",
    difficulty="all",
    metric="all",
    limit: int = 50,
    clear: bool = False,
):
    """Queue an update for the given specs and bosses."""
    response.headers["Cache-Control"] = "no-cache"

    payload = SpecRankingPayload(
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
    response: fastapi.Response,
    spec_slug: str,
    boss_slug: str,
    difficulty: str = "mythic",
    metric: str = "",
    dirty: bool = True,
):
    """Flag a Spec Ranking as dirty."""
    response.headers["Cache-Control"] = "no-cache"

    if not metric:
        spec = WowSpec.get(full_name_slug=spec_slug)
        metric = spec.role.metric if spec else "dps"

    spec_ranking = warcraftlogs_ranking.SpecRanking.get_or_create(
        spec_slug=spec_slug,
        boss_slug=boss_slug,
        difficulty=difficulty,
        metric=metric,
    )
    if spec_ranking:
        spec_ranking.dirty = dirty
        spec_ranking.save()

    return {
        "message": "success",
    }
