"""Handler to plan the next hour's Spec Ranking Refreshes and queue them."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.clients import sqs
from lorgs.clients.wcl import WarcraftlogsClient
from lorgs.data import GAME_VERSIONS
from lorgs.logger import logger
from lorgs.models import refresh_planner, selectors
from lorgs.models.base.s3 import s3client
from lorgs.models.dirty_marker import DirtyMarker
from lorgs.models.task_payloads import SpecRankingPayload
from lorgs.models.warcraftlogs_ranking import SpecRanking


if typing.TYPE_CHECKING:
    import datetime

    from lorgs.models.game_version import GameVersion


REFRESH_LIMIT = 50
"""Players loaded per queued Refresh."""


def get_ranking_payloads(game_version: GameVersion) -> dict[str, SpecRankingPayload]:
    """The `load_spec_rankings` payload of every Spec Ranking of the Game Version's current season, by S3 key."""
    data = game_version.data
    keys = selectors.expand_selectors(
        data,
        selectors.select_specs(data, selectors.ALL),
        selectors.select_bosses(data, selectors.ALL),
        selectors.ALL,
        selectors.ALL,
    )
    result: dict[str, SpecRankingPayload] = {}
    for key in keys:
        payload = SpecRankingPayload(
            game_version=game_version.name,
            spec_slug=key.spec.full_name_slug,
            boss_slug=key.boss.full_name_slug,
            difficulty=key.difficulty,
            metric=key.metric,
            limit=REFRESH_LIMIT,
        )
        s3_key = SpecRanking.get_key(
            game_version=payload.game_version,
            spec_slug=payload.spec_slug,
            boss_slug=payload.boss_slug,
            difficulty=payload.difficulty,
            metric=payload.metric,
        )
        result[s3_key] = payload
    return result


def list_last_modified(game_version: GameVersion) -> dict[str, datetime.datetime]:
    """S3 `LastModified` of every stored Spec Ranking of the Game Version's current season, by key."""
    prefix = f"{game_version.name}/{SpecRanking.get_table_name()}/{game_version.data.season.slug}/"
    result: dict[str, datetime.datetime] = {}
    for page in s3client.get_paginator("list_objects_v2").paginate(
        Bucket=SpecRanking.bucket,
        Prefix=prefix,
    ):
        for obj in page.get("Contents", []):
            result[obj["Key"]] = obj["LastModified"]
    return result


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
        candidates += refresh_planner.make_candidates(
            version_payloads,
            list_last_modified(game_version),
            DirtyMarker.list_flagged(game_version),
        )

    planned = refresh_planner.plan(candidates, budget)
    logger.info(
        "refresh plan: limit %s, spent %s, budget %s refreshes, %s candidates (%s dirty), %s planned",
        info.get("limitPerHour"),
        info.get("pointsSpentThisHour"),
        budget,
        len(candidates),
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
