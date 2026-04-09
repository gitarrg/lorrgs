"""Models for Top Rankings for a given Spec."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import datetime
import textwrap
import typing

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.clients import wcl
from lorgs.logger import logger
from lorgs.models import warcraftlogs_base
from lorgs.models.base.s3 import S3Model
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.warcraftlogs_boss import Boss
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_player import Player
from lorgs.models.warcraftlogs_report import Report
from lorgs.models.wow_spec import WowSpec


# Map Difficulty Names to Integers used in WCL
DIFFICULTY_IDS = {
    "normal": 3,
    "heroic": 4,
    "mythic": 5,
}


class SpecRanking(S3Model, warcraftlogs_base.wclclient_mixin):
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

    ##########################
    # Methods
    #
    @staticmethod
    def sort_reports(reports: list[Report]) -> list[Report]:
        """Sort the reports in place by the highest dps player."""

        def get_total(report: Report) -> float:
            top = 0.0
            for fight in report.fights:
                for player in fight.players:
                    top = max(top, player.total)
            return top

        return sorted(reports, key=get_total, reverse=True)

    ############################################################################
    # Query: Rankings
    #
    def get_query(self) -> str:
        """Return the Query to load the rankings for this Spec & Boss."""
        difficulty_id = DIFFICULTY_IDS.get(self.difficulty) or 5

        return textwrap.dedent(
            f"""\
        worldData
        {{
            encounter(id: {self.boss.id})
            {{
                characterRankings(
                    className: "{self.spec.wow_class.name_slug_cap}"
                    specName: "{self.spec.name_slug_cap}"
                    metric: {self.metric}
                    difficulty: {difficulty_id}
                    includeCombatantInfo: false
                )
            }}
        }}
        """
        )

    @utils.as_list
    def get_old_reports(self) -> typing.Generator[tuple[str, int, str], None, None]:
        """Return a list of unique keys to identify existing reports."""
        for report in self.reports:
            for fight in report.fights:
                for player in fight.players:
                    key = (report.report_id, fight.fight_id, player.name)
                    yield key

    def add_new_fight(self, ranking_data: wcl.CharacterRanking) -> Report | None:
        report_data = ranking_data.report

        if not report_data:
            return None

        # skip hidden reports
        if ranking_data.hidden:
            return None

        ################
        # Player
        player = Player(
            name=ranking_data.name,
            total=ranking_data.amount,
            spec_slug=self.spec_slug,
        )

        ################
        # Fight
        fight = Fight(
            fight_id=report_data.fightID,
            start_time=ranking_data.startTime,
            duration=ranking_data.duration,
            players=[player],
        )

        ################
        # Report
        report = Report(
            report_id=report_data.code,
            start_time=report_data.startTime,
            fights=[fight],
            region=ranking_data.server.region,
        )
        # self.reports.append(report)
        return report

    def add_new_fights(self, rankings: list[wcl.CharacterRanking]):
        """Add new Fights."""

        # build a map of old reports
        old_reports: dict[tuple[str, int, str], Report] = {}
        for report in self.reports:
            for fight in report.fights:
                for player in fight.players:
                    key = (report.report_id, fight.fight_id, player.name)
                    old_reports[key] = report

        # for key in keys:
        #     print(key)

        reports = []
        has_new = False

        for ranking_data in rankings:
            report_data = ranking_data.report

            ################
            # check if already in the list
            key = (report_data.code, report_data.fightID, ranking_data.name)
           
            # reuse
            if old_report := old_reports.get(key):
                print("new", key)
                reports.append(old_report)
                continue

            # new
            if new_report := self.add_new_fight(ranking_data):
                print("new", key)
                reports.append(new_report)
                has_new = True

        if has_new:
            self.reports = reports
        return

    def process_query_result(self, **query_result: typing.Any):
        """Process the Ranking Results.

        Expected Query:
        >>> {
        >>>     worldData: {
        >>>         encounter: {
        >>>             characterRankings: ....
        >>>         }
        >>>     }
        >>> }
        """
        # unwrap data
        query_result = query_result["worldData"]
        world_data = wcl.WorldData(**query_result)

        rankings = world_data.encounter.characterRankings.rankings
        self.add_new_fights(rankings)
        self.post_init()

    async def load_rankings(self) -> None:
        """Fetch the current Ranking Data"""
        # Build and run the query
        query = self.get_query()
        query_result = await self.client.query(query)
        self.process_query_result(**query_result)

    ############################################################################
    # Query: Fights
    #
    async def load_actors(self) -> None:
        """Load the Casts for all missing fights."""

        items_to_load: list[warcraftlogs_base.wclclient_mixin] = []

        for i, fight in enumerate(self.fights):

            if not fight.boss:
                fight.boss = Boss(boss_slug=self.boss_slug)
                fight.boss.fight = fight

            # Load Phases for Dynamic Bosses
            raid_boss = fight.boss.raid_boss
            if raid_boss.phase_type == RaidBoss.PhaseType.DYNAMIC and not fight.phases:
                items_to_load += [fight]

            # Only full load the first boss.
            if i == 0:
                if not fight.boss.casts:
                    items_to_load += [fight.boss]

            # load players
            for player in fight.players:
                if player and not player.casts:
                    items_to_load.append(player)

        logger.info(f"load {len(items_to_load)} items")
        if not items_to_load:
            return

        await self.load_many(items_to_load, raise_errors=False)  # type: ignore

    ############################################################################
    # Query: Both
    #
    async def load(self, limit=50, clear_old=False) -> None:
        """Get Top Ranks for a given boss and spec."""
        logger.info(f"{self.boss.name} vs. {self.spec.name} {self.spec.wow_class.name} START | limit={limit} | clear_old={clear_old}")

        if clear_old:
            self.reports = []

        # refresh the ranking data
        await self.load_rankings()

        # self.reports = self.sort_reports(self.reports)

        # enforce limit
        limit = limit or -1
        self.reports = self.reports[:limit]

        return
        # load the fights/players/casts
        await self.load_actors()
        logger.info("done")

        # update timestamp and mark as clean
        self.updated = datetime.datetime.now(datetime.timezone.utc)
        self.dirty = False
