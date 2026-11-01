"""Handler to plan the next hour's Spec Ranking Refreshes (dry run: logs the plan, queues nothing)."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.clients.wcl import WarcraftlogsClient
from lorgs.data import GAME_VERSIONS
from lorgs.logger import logger
from lorgs.models import refresh_planner, selectors
from lorgs.models.base.s3 import s3client
from lorgs.models.dirty_marker import DirtyMarker
from lorgs.models.warcraftlogs_ranking import SpecRanking


if typing.TYPE_CHECKING:
    import datetime

    from lorgs.models.game_version import GameVersion


def get_ranking_keys(game_version: GameVersion) -> list[str]:
    """The S3 key of every Spec Ranking of the Game Version's current season."""
    data = game_version.data
    keys = selectors.expand_selectors(
        data,
        selectors.select_specs(data, selectors.ALL),
        selectors.select_bosses(data, selectors.ALL),
        selectors.ALL,
        selectors.ALL,
    )
    return [
        SpecRanking.get_key(
            game_version=game_version.name,
            spec_slug=key.spec.full_name_slug,
            boss_slug=key.boss.full_name_slug,
            difficulty=key.difficulty,
            metric=key.metric,
        )
        for key in keys
    ]


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


async def plan_spec_rankings() -> tuple[bool, str]:
    """Work out which Spec Rankings to refresh this hour, across all enabled Game Versions, and log them."""
    info = await WarcraftlogsClient.get_instance().get_rate_info()
    budget = refresh_planner.get_budget(
        info.get("limitPerHour", 0),
        info.get("pointsSpentThisHour", 0),
    )

    candidates: list[refresh_planner.Candidate] = []
    for game_version in GAME_VERSIONS.values():
        if not game_version.updates_enabled:
            continue
        candidates += refresh_planner.make_candidates(
            get_ranking_keys(game_version),
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
    for candidate in planned:
        logger.info(
            "would refresh: %s (last refreshed %s%s)",
            candidate.key,
            candidate.last_refreshed or "never",
            f", dirty since {candidate.dirty_since}" if candidate.dirty_since else "",
        )
    return True, f"planned {len(planned)} of {len(candidates)}"


async def main(message: dict[str, str]):  # ruff: ignore[unused-function-argument]  # same interface as the other handlers
    """The message carries no data: the plan covers every enabled Game Version."""
    return await plan_spec_rankings()
