"""Models to store our list of full reports.."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import operator
import re
import typing
from collections import defaultdict
from collections.abc import Callable
from typing import Any, ClassVar

# IMPORT THIRD PARTY LIBRARIES
import pydantic
import typing_extensions

# IMPORT LOCAL LIBRARIES
from lorgs.models import base, warcraftlogs_report
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_player import Player  # ruff: ignore[typing-only-first-party-import]


if typing.TYPE_CHECKING:
    from lorgs.models.game_data import GameData


class FilterExpression(pydantic.BaseModel):
    attr: str
    op: str
    value: int

    OPS: ClassVar[dict[str, Callable[[Any, Any], bool]]] = {
        "eq": operator.eq,
        "lt": operator.lt,
        "lte": lambda a, b: bool(a <= b),
        "gt": operator.gt,
        "gte": lambda a, b: bool(a >= b),
    }

    VALID_OPS: ClassVar[list[str]] = list(OPS.keys())
    RE_KEY: ClassVar[str] = r"([\w\-]+)"  # expr to match the key/attr name. eg.: spec or role name
    RE_OPS: ClassVar[str] = r"|".join(VALID_OPS)
    RE_VAL: ClassVar[str] = r"\d+"
    QUERY_ARG_RE: ClassVar[str] = rf"(?P<attr>{RE_KEY})\.((?P<op>{RE_OPS})\.)?(?P<value>{RE_VAL})"

    @classmethod
    def parse_str(cls, expr: str) -> FilterExpression:
        """query: filter/check expression. eg.: "my_attr.lt.3" => "my_attr" is less than 3."""
        m = re.match(cls.QUERY_ARG_RE, expr)
        if not m:
            raise ValueError(f"invalid query arg: {expr}")
        return cls.model_validate(m.groupdict())

    def run(self, values: dict) -> bool:
        op = self.OPS[self.op]
        return op(values.get(self.attr, 0), self.value)


class FightComposition(typing_extensions.TypedDict):
    roles: dict[str, int]
    specs: dict[str, int]
    classes: dict[str, int]


def get_composition(players: typing.Iterable[Player], game_data: GameData) -> FightComposition:
    """Generate a Composition Dict from a list of Players."""
    players = players or []

    comp: FightComposition = {
        "roles": defaultdict(int),
        "specs": defaultdict(int),
        "classes": defaultdict(int),
    }

    for player in players:
        spec = game_data.get_spec(player.spec_slug)
        if not spec:
            continue
        comp["roles"][spec.role.code] += 1
        comp["classes"][spec.wow_class.name_slug] += 1
        comp["specs"][spec.full_name_slug] += 1

    comp["roles"] = dict(comp["roles"])
    comp["classes"] = dict(comp["classes"])
    comp["specs"] = dict(comp["specs"])
    return comp


class CompRankingFight(Fight):
    """A single Fight showing in the Comp Rankings."""

    composition: FightComposition | None = None

    damage_taken: int = 0
    deaths: int = 0


class CompRankingReport(warcraftlogs_report.Report):
    fights: list[CompRankingFight] = []  # ty: ignore[invalid-attribute-override]


class CompRanking(base.S3Model):
    """A Group/List of reports for a given Boss."""

    game_version: str
    """Name of the Game Version the ranking belongs to."""

    boss_slug: str
    # the nameslug of the boss

    # datetime: timetamp of last update
    updated: base.UTCDatetime = base.UTC_MIN

    reports: list[CompRankingReport] = []
    """all reports for this boss."""

    # Config
    key: typing.ClassVar[str] = "{game_version}/{table_name}/{boss_slug}"

    def sort_reports(self) -> None:
        self.reports = sort_reports(self.reports)


def sort_reports(reports: list[CompRankingReport]) -> list[CompRankingReport]:
    def key(report: CompRankingReport):
        if not report.fights:
            return ()
        fight = report.fights[0]
        return (fight.deaths, fight.damage_taken, fight.duration)

    return sorted(reports, key=key)
