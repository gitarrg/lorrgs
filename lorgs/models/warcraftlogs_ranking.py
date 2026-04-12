"""Models for Top Rankings for a given Spec."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import datetime
import typing

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models.base.s3 import S3Model
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.warcraftlogs_report import Report  # noqa: TC001 # pydantic requires this import
from lorgs.models.wow_spec import WowSpec


if typing.TYPE_CHECKING:
    from lorgs.models.warcraftlogs_fight import Fight
    from lorgs.models.warcraftlogs_player import Player


class SpecRanking(S3Model):
    # Fields
    spec_slug: str
    boss_slug: str
    difficulty: str = "mythic"
    metric: str = ""

    reports: list[Report] = []
    """Sorted Reports for this Spec & Boss."""

    updated: datetime.datetime = datetime.datetime.min
    dirty: bool = False

    # Config
    key: typing.ClassVar[str] = "{spec_slug}/{boss_slug}__{difficulty}__{metric}"

    def post_init(self) -> None:
        for report in self.reports:
            report.post_init()

    ##########################
    # Attributes
    #
    @property
    def spec(self) -> WowSpec:
        return WowSpec.get(full_name_slug=self.spec_slug)  # type: ignore

    @property
    def boss(self) -> RaidBoss:
        return RaidBoss.get(full_name_slug=self.boss_slug)  # type: ignore

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

