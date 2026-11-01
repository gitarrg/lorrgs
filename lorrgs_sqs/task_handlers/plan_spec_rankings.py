"""Handler to plan the next hour's Spec Ranking Refreshes and queue them."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import datetime
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.clients import sqs
from lorgs.clients.wcl import WarcraftlogsClient
from lorgs.data import GAME_VERSIONS
from lorgs.logger import logger
from lorgs.models import refresh_planner
from lorgs.models.ranking_status import get_candidates, get_ranking_payloads


if typing.TYPE_CHECKING:
    from lorgs.models.task_payloads import SpecRankingPayload


async def plan_spec_rankings(*, dry_run: bool = False) -> tuple[bool, str]:
    """Work out which Spec Rankings to refresh this hour, across all enabled Game Versions, and queue them.

    Last hour's tasks may still be queued: `SpecRanking.needs_refresh` turns those duplicates into cheap skips.
    """
    info = await WarcraftlogsClient.get_instance().get_rate_info()
    budget = refresh_planner.get_budget(
        info.get("limitPerHour", 0),
        info.get("pointsSpentThisHour", 0),
    )

    candidates: list[refresh_planner.Candidate] = []
    payloads: dict[str, SpecRankingPayload] = {}
    for game_version in GAME_VERSIONS.values():
        if not game_version.updates_enabled:
            continue
        version_payloads = get_ranking_payloads(game_version)
        payloads.update(version_payloads)
        candidates += get_candidates(game_version, version_payloads)

    now = datetime.datetime.now(datetime.UTC)
    due = [c for c in candidates if c.is_due(now)]
    planned = refresh_planner.plan(candidates, budget, now)
    logger.info(
        "refresh plan: limit %s, spent %s, budget %s refreshes, %s candidates (%s due, %s dirty), %s planned",
        info.get("limitPerHour"),
        info.get("pointsSpentThisHour"),
        budget,
        len(candidates),
        len(due),
        sum(1 for c in candidates if c.dirty_since),
        len(planned),
    )

    # queue per Game Version, in plan order, in that Game Version's FIFO message group
    by_version: dict[str, list[SpecRankingPayload]] = {}
    for candidate in planned:
        payload = payloads[candidate.key].model_copy(update={"dirty": candidate.dirty_since is not None})
        by_version.setdefault(payload.game_version, []).append(payload)
        logger.info(
            "%s: %s (last refreshed %s%s)",
            "would refresh" if dry_run else "refresh",
            candidate.key,
            candidate.last_refreshed or "never",
            f", dirty since {candidate.dirty_since}" if candidate.dirty_since else "",
        )

    if not dry_run:
        for name, version_payloads in by_version.items():
            sqs.send_message_batch(version_payloads, message_group=f"{name}-load_spec_rankings")

    verb = "planned" if dry_run else "queued"
    message = f"{verb} {len(planned)} of {len(candidates)} (budget {budget})"
    logger.info(message)
    return True, message


async def main(message: dict[str, str]):  # ruff: ignore[unused-function-argument]  # same interface as the other handlers
    """The message carries no data: the plan covers every enabled Game Version."""
    return await plan_spec_rankings()
