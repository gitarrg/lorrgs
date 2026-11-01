"""Dirty markers: small S3 objects flagging Spec Rankings that need a full reload.

A marker sits next to the rankings under a sibling prefix (`{game_version}/dirty_marker/...`),
so the Refresh Planner finds every Dirty ranking of a Game Version with one listing instead of
reading each ranking. The marker's `LastModified` is when the ranking was flagged.
"""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.data import get_game_version
from lorgs.models.base.s3 import S3Model, s3client
from lorgs.models.warcraftlogs_ranking import SpecRanking


if typing.TYPE_CHECKING:
    import datetime

    from lorgs.models.game_version import GameVersion


class DirtyMarker(S3Model):
    """Flags the Spec Ranking with the same game version, spec, boss, difficulty and metric as Dirty."""

    game_version: str
    spec_slug: str
    boss_slug: str
    difficulty: str
    metric: str = ""

    key: typing.ClassVar[str] = (
        "{game_version}/{table_name}/{season}/{spec_slug}/"  # path
        "{boss_slug}__{difficulty}__{metric}"  # filename
    )

    @classmethod
    def get_key(cls, **kwargs: typing.Any) -> str:
        """The current season of the marker's Game Version, unless a season is passed in."""
        if "game_version" in kwargs:
            kwargs["season"] = get_game_version(kwargs["game_version"]).data.season.slug

        return super().get_key(**kwargs)

    def clear(self) -> None:
        """Remove the marker. Fine if there is none."""
        s3client.delete_object(Bucket=self.bucket, Key=self.get_key(**dict(self)))

    @classmethod
    def list_flagged(cls, game_version: GameVersion) -> dict[str, datetime.datetime]:
        """When each Dirty Spec Ranking of the Game Version's current season was flagged, by Spec Ranking key."""
        prefix = f"{game_version.name}/{cls.get_table_name()}/{game_version.data.season.slug}/"
        ranking_prefix = f"{game_version.name}/{SpecRanking.get_table_name()}/{game_version.data.season.slug}/"

        result: dict[str, datetime.datetime] = {}
        for page in s3client.get_paginator("list_objects_v2").paginate(Bucket=cls.bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                result[ranking_prefix + obj["Key"].removeprefix(prefix)] = obj["LastModified"]
        return result
