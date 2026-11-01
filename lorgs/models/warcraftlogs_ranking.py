"""Models for Top Rankings for a given Spec."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import datetime
import typing

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.data import get_game_version
from lorgs.models.base import UTC_MIN, UTCDatetime
from lorgs.models.base.s3 import S3Model
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.warcraftlogs_report import Report  # ruff: ignore[typing-only-first-party-import] # pydantic requires this import


if typing.TYPE_CHECKING:
    from lorgs.models.dirty_marker import DirtyMarker
    from lorgs.models.warcraftlogs_fight import Fight
    from lorgs.models.warcraftlogs_player import Player


class SpecRanking(S3Model):
    game_version: str
    """Name of the Game Version the ranking belongs to."""

    spec_slug: str
    boss_slug: str
    difficulty: str
    metric: str = ""

    reports: list[Report] = []
    """Sorted Reports for this Spec & Boss."""

    updated: UTCDatetime = UTC_MIN

    # Config
    key: typing.ClassVar[str] = (
        "{game_version}/{table_name}/{season}/{spec_slug}/"  # path
        "{boss_slug}__{difficulty}__{metric}"  # filename
    )

    refresh_after: typing.ClassVar[datetime.timedelta] = datetime.timedelta(hours=2)

    @classmethod
    def get_key(cls, **kwargs: typing.Any) -> str:
        """The current season of the ranking's Game Version, unless a season is passed in."""
        if "game_version" in kwargs:
            game_version = get_game_version(kwargs["game_version"])
            kwargs["season"] = game_version.data.season.slug

        return super().get_key(**kwargs)

    @property
    def dirty_marker(self) -> DirtyMarker:
        """The marker that flags this ranking as Dirty. It exists in S3 only while the ranking is flagged."""
        from lorgs.models.dirty_marker import DirtyMarker  # ruff: ignore[import-outside-top-level]  # it imports this module

        return DirtyMarker(
            game_version=self.game_version,
            spec_slug=self.spec_slug,
            boss_slug=self.boss_slug,
            difficulty=self.difficulty,
            metric=self.metric,
        )

    def needs_refresh(self, now: datetime.datetime | None = None) -> bool:
        """Whether this ranking should be re-fetched from Warcraft Logs.

        A ranking is refreshed only when its last Refresh is more than
        ``refresh_after`` old, however many reports it holds: a boss or spec with
        fewer ranked logs than the limit must not cost a Refresh on every run.
        Dirty rankings are flagged by a marker (see `DirtyMarker`), not known here.
        """
        if now is None:
            now = datetime.datetime.now(datetime.UTC)
        return now - self.updated > self.refresh_after

    def post_init(self) -> None:
        for report in self.reports:
            report.post_init()

    ##########################
    # Attributes
    #
    @property
    def fights(self) -> list[Fight]:
        return utils.flatten(report.fights for report in self.reports)

    @property
    def players(self) -> list[Player]:
        return utils.flatten(fight.players for fight in self.fights)

    def get_top_fight(self) -> Fight | None:
        try:
            return self.reports[0].fights[0]
        except IndexError:
            return None

    def get_top_player(self) -> Player | None:
        try:
            return self.reports[0].fights[0].players[0]
        except IndexError:
            return None

    @property
    def raid_difficulty(self) -> RaidDifficulty:
        return RaidDifficulty(self.difficulty)
