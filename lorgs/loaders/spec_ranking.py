"""Loader for SpecRanking data from WarcraftLogs."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import asyncio
import datetime
import textwrap
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.clients import wcl
from lorgs.clients.wcl.client import WarcraftlogsClient
from lorgs.logger import logger
from lorgs.models.warcraftlogs_boss import Boss
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_player import Player
from lorgs.models.warcraftlogs_report import Report

from .base_loader import BaseLoader
from .boss_loader import BossLoader
from .fight_phases import FightPhasesLoader
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
                    partition: 1
                )
            }}
        }}
        """
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
        old_reports: dict[tuple[str, int, str], Report] = {}
        for report in self.ranking.reports:
            for fight in report.fights:
                for player in fight.players:
                    key = (report.report_id, fight.fight_id, player.name)
                    old_reports[key] = report

        # merge new rankings
        self.ranking.reports = []
        for ranking_data in rankings:
            report_data = ranking_data.report

            key = (report_data.code, report_data.fightID, ranking_data.name)

            # check if the report is already in the old reports
            if old_report := old_reports.get(key):
                self.ranking.reports.append(old_report)
                continue

            # new ranking
            if new_report := self._ranking_to_report(ranking_data):
                self.ranking.reports.append(new_report)

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
            raise_errors: If True, raise errors.

        """
        logger.info(f"{self.ranking.boss.name} vs. {self.ranking.spec.name} START | {limit=} | {clear_old=}")

        ###########################
        # Step 1: Fetch rankings
        if clear_old:
            self.ranking.reports = []

        # fetch rankings
        client = client or WarcraftlogsClient.get_instance()
        client.raise_errors = False  # to skip invalid reports leftover in the ranking (eg.: reports which have been made private)
        await super().load(client=client)

        # enforce limit
        if limit > 0:
            self.ranking.reports = self.ranking.reports[:limit]

        ##############################################
        # secondary tasks
        loaders: list[BaseLoader] = []

        # load phases for all fights
        for fight in self.ranking.fights:
            loaders.append(FightPhasesLoader(fight))

        # load boss for first fight
        if (top_fight := self.ranking.get_top_fight()) and top_fight.boss:
            loaders.append(BossLoader(top_fight.boss))

        # load actors
        for player in self.ranking.players:
            loaders.append(PlayerLoader(player))

        loaders = [loader for loader in loaders if loader.needs_load()]
        logger.info(f"load {len(loaders)} items")
        if loaders:
            await asyncio.gather(*[loader.load(client=client) for loader in loaders])

        self.ranking.updated = datetime.datetime.now(datetime.UTC)
        self.ranking.dirty = False
        logger.info("done")
