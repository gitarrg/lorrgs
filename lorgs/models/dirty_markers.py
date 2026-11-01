"""Dirty markers: empty S3 objects flagging Spec Rankings that need a full reload.

A marker sits next to the rankings under a sibling prefix (`{game_version}/spec_ranking_dirty/...`),
so the Refresh Planner finds every Dirty ranking of a Game Version with one listing instead of
reading each ranking. The marker's `LastModified` is when the ranking was flagged.
"""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.models.base.s3 import s3client
from lorgs.models.warcraftlogs_ranking import SpecRanking


if typing.TYPE_CHECKING:
    import datetime

    from lorgs.models.game_version import GameVersion


TABLE_SUFFIX = "_dirty"
"""Appended to the Spec Ranking table name to get the marker prefix."""


def marker_key(ranking_key: str) -> str:
    """The marker key of a Spec Ranking key: `retail/spec_ranking/...` -> `retail/spec_ranking_dirty/...`."""
    game_version, table, rest = ranking_key.split("/", 2)
    return f"{game_version}/{table}{TABLE_SUFFIX}/{rest}"


def ranking_key(marker_key: str) -> str:
    """The Spec Ranking key of a marker key."""
    game_version, table, rest = marker_key.split("/", 2)
    return f"{game_version}/{table.removesuffix(TABLE_SUFFIX)}/{rest}"


def flag(key: str) -> None:
    """Flag the Spec Ranking with this S3 key as Dirty."""
    s3client.put_object(Bucket=SpecRanking.bucket, Key=marker_key(key), Body=b"")


def clear(key: str) -> None:
    """Remove the Dirty flag of the Spec Ranking with this S3 key. Fine if it has none."""
    s3client.delete_object(Bucket=SpecRanking.bucket, Key=marker_key(key))


def list_flagged(game_version: GameVersion) -> dict[str, datetime.datetime]:
    """When each Dirty Spec Ranking of the Game Version's current season was flagged, by Spec Ranking key."""
    table = SpecRanking.get_table_name() + TABLE_SUFFIX
    prefix = f"{game_version.name}/{table}/{game_version.data.season.slug}/"
    result: dict[str, datetime.datetime] = {}
    for page in s3client.get_paginator("list_objects_v2").paginate(Bucket=SpecRanking.bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            result[ranking_key(obj["Key"])] = obj["LastModified"]
    return result
