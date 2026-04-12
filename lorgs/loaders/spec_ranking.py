"""Loader for SpecRanking data from WarcraftLogs."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import asyncio
import datetime
import textwrap
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.clients import wcl
from lorgs.loaders.actor import loader_for
from lorgs.loaders.base_loader import BaseLoader
from lorgs.logger import logger
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.warcraftlogs_boss import Boss
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_player import Player
from lorgs.models.warcraftlogs_report import Report

if typing.TYPE_CHECKING:
    from lorgs.clients.wcl.client import WarcraftlogsClient
    from lorgs.models.warcraftlogs_actor import BaseActor
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

    def collect_actors_to_load(self) -> list[typing.Any]:
        items: set[BaseActor] = set()

        for i, fight in enumerate(self.ranking.fights):
            # load phases if they are dynamic
            if (
                not fight.phases
                and fight.boss
                and fight.boss.raid_boss
                and fight.boss.raid_boss.phase_type == RaidBoss.PhaseType.DYNAMIC
            ):
                items.add(fight.boss)
                print("added boss (dynamic)", fight.boss.boss_slug)

            # full load boss for the first fight
            if i == 0:
                items.add(fight.boss)

            # load players
            for player in fight.players:
                items.add(player)

        items = {item for item in items if item and not item.casts}
        return list(items)

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
        await super().load(client=client, raise_errors=raise_errors)

        # enforce limit
        if limit > 0:
            self.ranking.reports = self.ranking.reports[:limit]

        ###########################
        # Step 2: Load actors
        actors = self.collect_actors_to_load()
        logger.info(f"load {len(actors)} items")
        if actors:
            tasks = [loader_for(actor).load(client=client, raise_errors=raise_errors) for actor in actors]
            await asyncio.gather(*tasks)

        logger.info("done")

        self.ranking.updated = datetime.datetime.now(datetime.UTC)
        self.ranking.dirty = False
