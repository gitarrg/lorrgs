"""Models to store our list of full reports.."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import operator
import re
import textwrap
import typing
from collections import defaultdict
import datetime
from typing import Any, Callable, ClassVar, Optional
import typing_extensions

# IMPORT THIRD PARTY LIBRARIES
import pydantic

# IMPORT LOCAL LIBRARIES
from lorgs.clients import wcl
from lorgs.logger import logger
from lorgs.models import base, warcraftlogs_base, warcraftlogs_report
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.warcraftlogs_boss import Boss
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_player import Player
from lorgs.models.warcraftlogs_report import Report
from lorgs.models.wow_spell import SpellTag, WowSpell, build_spell_query


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
    def parse_str(cls, expr: str) -> "FilterExpression":
        """
        query: filter/check expression. eg.: "my_attr.lt.3" => "my_attr" is less than 3.

        """
        m = re.match(cls.QUERY_ARG_RE, expr)
        if not m:
            raise ValueError(f"invalid query arg: {expr}")
        return cls.parse_obj(m.groupdict())

    def run(self, values: dict) -> bool:
        op = self.OPS[self.op]
        return op(values.get(self.attr, 0), self.value)


class FightComposition(typing_extensions.TypedDict):
    roles: dict[str, int]
    specs: dict[str, int]
    classes: dict[str, int]


def get_composition(players: typing.Iterable[Player]) -> FightComposition:
    """Generate a Composition Dict from a list of Players."""
    players = players or []

    comp: FightComposition = {
        "roles": defaultdict(int),
        "specs": defaultdict(int),
        "classes": defaultdict(int),
    }

    for player in players:
        comp["roles"][player.spec.role.code] += 1
        comp["classes"][player.spec.wow_class.name_slug] += 1
        comp["specs"][player.spec.full_name_slug] += 1

    comp["roles"] = dict(comp["roles"])
    comp["classes"] = dict(comp["classes"])
    comp["specs"] = dict(comp["specs"])
    return comp


class CompRankingFight(Fight):
    """A single Fight showing in the Comp Rankings."""

    composition: Optional[FightComposition] = None

    damage_taken: int = 0
    deaths: int = 0

    def get_query_parts(self) -> list[str]:
        spells = [spell for spell in WowSpell.list() if SpellTag.RAID_CD in spell.tags]
        filter_expr = build_spell_query(*spells)
        query = f'events({self.table_query_args}, filterExpression: "{filter_expr}") {{data}}'

        parts = super().get_query_parts()
        parts.append(query)
        return parts

    async def load(self, *args, **kwargs):
        await super().load(*args, **kwargs)
        if self.boss:
            await self.boss.load(*args, **kwargs)

    def process_query_result(self, **query_result: typing.Any):
        super().process_query_result(**query_result)
        self.composition = get_composition(self.players)


class CompRankingReport(warcraftlogs_report.Report):
    fights: list[CompRankingFight] = []  # type: ignore # mypy doesn't like reassignment


class CompRanking(base.S3Model, warcraftlogs_base.wclclient_mixin):
    """A Group/List of reports for a given Boss."""

    boss_slug: str
    # the nameslug of the boss

    # datetime: timetamp of last update
    updated: datetime.datetime = datetime.datetime.min

    reports: list[CompRankingReport] = []
    """all reports for this boss."""

    # Config
    key: typing.ClassVar[str] = "{boss_slug}"

    @property
    def boss(self) -> Optional[RaidBoss]:
        return RaidBoss.get(full_name_slug=self.boss_slug)

    ############################################################################
    # Query
    #
    def get_query(self, metric: str = "execution", page: int = 1) -> str:
        """Get the Query to load this Fight Rankings."""
        if not self.boss:
            raise ValueError(f"Unknown Boss: {self.boss_slug}")

        return textwrap.dedent(
            f"""
            worldData
            {{
                encounter(id: {self.boss.id})
                {{
                    fightRankings(
                        metric: {metric}
                        page: {page}
                    )
                }}
            }}
            """
        )

    def add_report(self, fight_data: wcl.FightRankingsFight):
        """Add a new Report/Fight to the Ranking."""
        boss = Boss(boss_slug=self.boss_slug)

        fight = CompRankingFight(
            fight_id=fight_data.report.fightID,
            start_time=fight_data.startTime,
            duration=fight_data.duration,
            boss=boss,
            players=[],
            damage_taken=fight_data.damageTaken,
            deaths=fight_data.deaths,
        )

        report = CompRankingReport(
            report_id=fight_data.report.code,
            start_time=fight_data.report.startTime,
            fights=[fight],
        )

        self.reports.append(report)

    async def load_page(self, page=0, metric: str = "execution"):
        """Get Top Fights for a given encounter."""

        # build a list of old Reports
        old_reports: list[tuple[str, int]] = []
        for report in self.reports:
            for fight in report.fights:
                old_reports.append((report.report_id, fight.fight_id))

        # execute the query
        query = self.get_query(metric=metric, page=page)
        query_result = await self.client.query(query)
        query_result = query_result["worldData"]

        # parse data
        world_data = wcl.WorldData(**query_result)
        rankings = world_data.encounter.fightRankings

        # add fights
        for fight_data in rankings.rankings:
            key = (fight_data.report.code, fight_data.report.fightID)
            if key not in old_reports:
                self.add_report(fight_data)

    async def load(self, limit: int = 0, clear_old: bool = False, page=1):
        """Fetch reports for this BossRanking.

        params:
            limit (int): maximum number of reports to load.
            page (int): page number to load (starts from 1).
            clear_old (bool): if true old reports will be deleted.

        """

        # copy the list, to make pydantic belive it has changed
        self.reports = self.reports[:]

        # old reports
        if clear_old:
            self.reports = []
        await self.load_page(page=page)
        if limit:
            self.reports = self.reports[:limit]

        # 1) Load Fights
        fights_to_load = []
        for report in self.reports:
            for fight in report.fights:
                if not fight.players:
                    fights_to_load.append(fight)

        logger.info(f"Load {len(fights_to_load)} Fights")
        await self.load_many(fights_to_load, raise_errors=False)  # type: ignore

        self.sort_reports()
        self.updated = datetime.datetime.utcnow()

    def sort_reports(self) -> None:
        self.reports = sort_reports(self.reports)


def sort_reports(reports: list[CompRankingReport]) -> list[CompRankingReport]:
    def key(report: CompRankingReport):
        if not report.fights:
            return ()
        fight = report.fights[0]
        return (fight.deaths, fight.damage_taken, fight.duration)

    return sorted(reports, key=key)
