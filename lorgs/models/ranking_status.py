"""Which Spec Rankings a Game Version has, when each was last refreshed and which are Dirty.

Shared by the Refresh Planner task and the status endpoint, so both see the rankings the same way.
"""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
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


def get_candidates(
    game_version: GameVersion,
    payloads: dict[str, SpecRankingPayload] | None = None,
) -> list[refresh_planner.Candidate]:
    """Every Spec Ranking of the Game Version with its last refresh and Dirty flag, as the Refresh Planner sees them."""
    if payloads is None:
        payloads = get_ranking_payloads(game_version)
    return refresh_planner.make_candidates(
        payloads,
        list_last_modified(game_version),
        DirtyMarker.list_flagged(game_version),
    )
