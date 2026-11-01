"""Handler to Load Spec Rankings."""

from __future__ import annotations

# IMPORT LOCAL LIBRARIES
from lorgs.clients.wcl import WarcraftlogsClient
from lorgs.loaders.spec_ranking import SpecRankingLoader
from lorgs.logger import logger
from lorgs.models import dirty_markers, selectors, warcraftlogs_ranking
from lorgs.models.task_payloads import SpecRankingPayload
from lorrgs_sqs.exceptions import TaskValidationError


POINTS_RESERVE = 0.2
"""Share of the hourly Warcraft Logs points kept for User Reports: Spec Rankings skip below it."""


async def has_points_to_spare(client: WarcraftlogsClient) -> bool:
    """Whether more than `POINTS_RESERVE` of this hour's points are left. True when Warcraft Logs does not say."""
    info = await client.get_rate_info()
    limit = info.get("limitPerHour", 0)
    if not limit:
        return True
    points_left = limit - info.get("pointsSpentThisHour", 0)
    if points_left > limit * POINTS_RESERVE:
        return True
    logger.warning("low on points: %s of %s left, resets in %ss", points_left, limit, info.get("pointsResetIn"))
    return False


async def load_spec_rankings(payload: SpecRankingPayload) -> tuple[bool, str]:
    """Load the Spec Ranking Data from Warcraftlogs and save it to the Database."""
    logger.info(f"loading: {payload} vs {payload.spec_slug} | {payload.difficulty=}")

    game_version = payload.get_game_version()
    game_data = game_version.data
    if not game_data.get_boss(full_name_slug=payload.boss_slug):
        raise TaskValidationError("invalid boss")
    spec = game_data.get_spec(payload.spec_slug)
    if not spec:
        raise TaskValidationError("invalid spec")

    ################################
    # get spec ranking object
    ranking = warcraftlogs_ranking.SpecRanking.get_or_create(
        game_version=game_version.name,
        boss_slug=payload.boss_slug,
        spec_slug=payload.spec_slug,
        difficulty=game_data.resolve_difficulty(payload.boss_slug, payload.difficulty),
        metric=payload.metric or selectors.default_metric(spec),
    )

    clear = payload.clear or payload.dirty
    needs_refresh = clear or ranking.needs_refresh()
    if not needs_refresh:
        logger.info(f"already updated: {payload=}")
        return True, "already updated"

    # skipped, not retried: the next scheduled refresh picks the ranking up again
    client = WarcraftlogsClient.get_instance()
    if not await has_points_to_spare(client):
        return True, "skipped: low on points"

    await SpecRankingLoader(
        ranking,
        game_version,
    ).load(
        client=client,
        limit=payload.limit,
        clear_old=clear,
    )
    ranking.save()
    if payload.dirty:
        dirty_markers.clear(ranking.get_key(**dict(ranking)))
    return True, "done"


async def main(message: dict[str, str]):
    """Load the Spec Ranking Data from Warcraftlogs and save it to the Database."""
    message_body = message.get("body")
    if not message_body:
        raise TaskValidationError("No message body.")

    payload = SpecRankingPayload.model_validate_json(message_body, extra="ignore")
    return await load_spec_rankings(payload)
