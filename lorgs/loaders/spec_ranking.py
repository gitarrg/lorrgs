"""Loader for SpecRanking data from WarcraftLogs."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import asyncio
import datetime
import textwrap
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.clients import wcl
from lorgs.clients.wcl.client import PrivateReportError, UnknownReportError, WarcraftlogsClient
from lorgs.logger import logger
from lorgs.models.warcraftlogs_boss import Boss
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_player import Player
from lorgs.models.warcraftlogs_report import Report

from .base_loader import BaseLoader
from .boss_loader import BossLoader
from .fight_phases import FightPhasesLoader, correct_loaded_phases
from .player_loader import PlayerLoader


if typing.TYPE_CHECKING:
    from lorgs.models.warcraftlogs_ranking import SpecRanking


class SpecRankingLoader(BaseLoader):
    """Loads spec ranking data and actor events from WarcraftLogs."""

    def __init__(self, ranking: SpecRanking) -> None:
        self.ranking = ranking

    def get_query(self) -> str:
        return textwrap.dedent(
            f"""\
        worldData
        {{
            encounter(id: {self.ranking.boss.id})
            {{
                characterRankings(
                    className: "{self.ranking.spec.wow_class.name_slug_cap}"
                    specName: "{self.ranking.spec.name_slug_cap}"
                    metric: {self.ranking.metric}
                    difficulty: {self.ranking.raid_difficulty.value}
                    includeCombatantInfo: false
                )
            }}
        }}
        """,
        )

    def _ranking_to_report(self, ranking_data: wcl.CharacterRanking) -> Report | None:
        """Convert a ranking data to a report."""
        report_data = ranking_data.report
        if not report_data:
            return None

        # skip hidden reports
        if ranking_data.hidden:
            return None

        player = Player(
            name=ranking_data.name,
            total=ranking_data.amount,
            spec_slug=self.ranking.spec_slug,
        )

        boss = Boss(boss_slug=self.ranking.boss_slug)

        fight = Fight(
            fight_id=report_data.fightID,
            start_time=ranking_data.startTime,
            duration=ranking_data.duration,
            players=[player],
            boss=boss,
        )

        return Report(
            report_id=report_data.code,
            start_time=report_data.startTime,
            fights=[fight],
            region=ranking_data.server.region,
        )

    def merge_rankings(self, rankings: list[wcl.CharacterRanking]) -> None:
        """Combine old and new rankings.

        # Todo:
            - consider removing duplicates of the same character
              (would have to change key to character id and make sure we
              always use that persons best parse)

        """
        # build a map of old reports
        old_reports: set[tuple[str, int, str]] = set()
        for report in self.ranking.reports:
            for fight in report.fights:
                for player in fight.players:
                    key = (report.report_id, fight.fight_id, player.name)
                    old_reports.add(key)

        # merge new rankings
        for ranking_data in rankings:
            report_data = ranking_data.report

            key = (report_data.code, report_data.fightID, ranking_data.name)

            # check if the report has already been loaded
            if key in old_reports:
                continue

            # new ranking
            if new_report := self._ranking_to_report(ranking_data):
                self.ranking.reports.append(new_report)

        # sort
        def get_total(report: Report) -> float:
            return sum(player.total for fight in report.fights for player in fight.players)
        self.ranking.reports.sort(key=get_total, reverse=True)

    def process_query_result(self, query_result: dict[str, typing.Any]) -> None:
        query_result = query_result["worldData"]
        world_data = wcl.WorldData(**query_result)

        rankings = world_data.encounter.characterRankings.rankings
        self.merge_rankings(rankings)
        self.ranking.post_init()

    # ------------------------------------------------------------------
    # Actor loading
    # ------------------------------------------------------------------

    async def load(
        self,
        client: WarcraftlogsClient | None = None,
        *,
        limit: int = 50,
        clear_old: bool = False,
    ) -> None:
        """Load the Spec Ranking data from WarcraftLogs.

        Args:
            client: WarcraftlogsClient instance to use for the request.
            limit: Maximum number of reports to load.
            clear_old: If True, old reports will be deleted.

        """
        logger.info(f"{self.ranking.boss.name} vs. {self.ranking.spec.name} START | {limit=} | {clear_old=}")

        ###########################
        # Step 1: Fetch rankings
        if clear_old:
            self.ranking.reports = []

        # fetch rankings
        client = client or WarcraftlogsClient.get_instance()
        await super().load(client=client)

        # enforce limit
        if limit > 0:
            self.ranking.reports = self.ranking.reports[:limit]

        ##############################################
        # Load each report separately so a private or deleted one can be dropped.
        top_fight = self.ranking.get_top_fight()
        skipped = await asyncio.gather(
            *[SpecRankingLoader._load_report(report, client, top_fight) for report in self.ranking.reports],
        )
        skipped_ids = {report_id for report_id in skipped if report_id}
        if skipped_ids:
            self.ranking.reports = [report for report in self.ranking.reports if report.report_id not in skipped_ids]

        self.ranking.updated = datetime.datetime.now(datetime.UTC)
        self.ranking.dirty = False
        logger.info("done")

    @staticmethod
    async def _load_report(
        report: Report,
        client: WarcraftlogsClient,
        top_fight: Fight | None,
    ) -> str | None:
        """Load one report. Return its id when Warcraft Logs refuses it."""
        loaders: list[BaseLoader] = []
        boss_fights: list[Fight] = []
        for fight in report.fights:
            loaders.append(FightPhasesLoader(fight))
            if top_fight is not None and fight is top_fight and top_fight.boss:
                boss_loader = BossLoader(top_fight.boss)
                if boss_loader.needs_load():
                    boss_fights.append(fight)
                loaders.append(boss_loader)
            for player in fight.players:
                loaders.append(PlayerLoader(player))

        loaders = [loader for loader in loaders if loader.needs_load()]
        try:
            if loaders:
                await asyncio.gather(*[loader.load(client=client) for loader in loaders])
            else:
                await client.query(f'reportData {{ report(code: "{report.report_id}") {{ code }} }}')
        except (PrivateReportError, UnknownReportError):
            logger.warning("Skipping report %s during spec ranking refresh", report.report_id)
            return report.report_id

        for fight in boss_fights:
            correct_loaded_phases(fight)
        return None
