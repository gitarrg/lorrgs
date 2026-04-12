"""API Routes to get and update Comp Rankings."""
from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs.clients import sqs
from lorgs.models.task_payloads import CompRankingPayload
from lorgs.models.warcraftlogs_comp_ranking import CompRanking, CompRankingFight, FilterExpression


router = fastapi.APIRouter(tags=["comp_ranking"])


@router.get("/comp_ranking/{boss_slug}", response_model_exclude_unset=True)
async def get_comp_ranking(
    response: fastapi.Response,
    boss_slug: str,
    # Query Params
    limit: int = 20,
    roles: list[str] = fastapi.Query([], alias="role"),
    specs: list[str] = fastapi.Query([], alias="spec"),
    killtime_min: int = 0,
    killtime_max: int = 0,
) -> CompRanking:
    """Fetch comp rankings for a given boss encounter.

    Args:
        boss_slug (str): name of the boss (full_name_slug)
    """
    # shorter cache timeout for the start of the tier (where frequent changes happen)
    response.headers["Cache-Control"] = "max-age=300"

    # fetch the data
    comp_ranking = CompRanking.get(boss_slug=boss_slug)
    if not comp_ranking:
        raise fastapi.HTTPException(status_code=404, detail="Not Found.")

    def fight_filter(fight: CompRankingFight):
        if killtime_min:
            if fight.duration < (killtime_min * 1000):
                return False
        if killtime_max:
            if fight.duration > (killtime_max * 1000):
                return False

        if not fight.composition:
            return False

        for spec_expr in specs:
            expr = FilterExpression.parse_str(spec_expr)
            if not expr.run(fight.composition["specs"]):
                return False

        for role_expr in roles:
            expr = FilterExpression.parse_str(role_expr)
            if not expr.run(fight.composition["roles"]):
                return False

        return True

    for report in comp_ranking.reports:
        report.fights = [fight for fight in report.fights if fight_filter(fight)]

    comp_ranking.reports = [r for r in comp_ranking.reports if r.fights]
    comp_ranking.reports = comp_ranking.reports[:limit]
    return comp_ranking


################################################################################
# Tasks
#
@router.get("/comp_ranking/load/{boss_slug}")
async def task_load_comp_rankings(
    response: fastapi.Response, boss_slug: str = "all", limit: int = 50, clear: bool = False
):
    """Submit a scheduled task to update a single or all Comp Rankings."""
    response.headers["Cache-Control"] = "no-cache"

    payloads: list[CompRankingPayload] = []

    if clear:
        payloads.append(CompRankingPayload(boss_slug=boss_slug, clear=True))

    pages = (limit // 50)
    for page in range(pages):
        payloads.append(CompRankingPayload(
            boss_slug=boss_slug,
            page=page + 1,  # +1 because pages start at one.
        ))

    if payloads:
        sqs.send_message_batch(payloads=payloads)

    return {
        "message": "task queued",
        "payloads": payloads,
    }
