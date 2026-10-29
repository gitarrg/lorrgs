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
from .fight_phases import (
    FightPhasesLoader,
    correct_loaded_phases,
    fights_ready_for_phase_correction,
    queue_boss_loader,
)
from .player_loader import PlayerLoader


if typing.TYPE_CHECKING:
    from lorgs.models.game_data import GameData
    from lorgs.models.game_version import GameVersion
    from lorgs.models.raid_boss import RaidBoss
    from lorgs.models.warcraftlogs_ranking import SpecRanking
    from lorgs.models.wow_spec import WowSpec


class SpecRankingLoader(BaseLoader):
    """Loads spec ranking data and actor events from WarcraftLogs."""

    def __init__(self, ranking: SpecRanking, game_version: GameVersion) -> None:
        if ranking.game_version != game_version.name:
            msg = f"Ranking belongs to Game Version {ranking.game_version!r}, not {game_version.name!r}"
            raise ValueError(
                msg,
            )
        super().__init__(game_version.data)
        self.ranking = ranking

    @property
    def boss(self) -> RaidBoss:
        boss = self.game_data.get_boss(full_name_slug=self.ranking.boss_slug)
        if boss is None:
            raise ValueError(f"Unknown Boss: {self.ranking.boss_slug}")
        return boss

    @property
    def spec(self) -> WowSpec:
        spec = self.game_data.get_spec(self.ranking.spec_slug)
        if spec is None:
            raise ValueError(f"Unknown Spec: {self.ranking.spec_slug}")
        return spec

    def get_query(self) -> str:
        return textwrap.dedent(
            f"""\
        worldData
        {{
            encounter(id: {self.boss.id})
            {{
                characterRankings(
                    className: "{self.spec.wow_class.name_slug_cap}"
                    specName: "{self.spec.name_slug_cap}"
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
        logger.info(f"{self.boss.name} vs. {self.spec.name} START | {limit=} | {clear_old=}")

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
        game_data = self.game_data
        skipped = await asyncio.gather(
            *[SpecRankingLoader._load_report(report, game_data, client, top_fight) for report in self.ranking.reports],
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
        game_data: GameData,
        client: WarcraftlogsClient,
        top_fight: Fight | None,
    ) -> str | None:
        """Load one report. Return its id when Warcraft Logs refuses it."""
        loaders: list[BaseLoader] = []
        fights_loading_boss: list[Fight] = []
        fights_loading_phases: list[Fight] = []
        for fight in report.fights:
            phase_loader = FightPhasesLoader(fight, game_data)
            if phase_loader.needs_load():
                fights_loading_phases.append(fight)
            loaders.append(phase_loader)
            if top_fight is not None and fight is top_fight:
                queue_boss_loader(fight, loaders, fights_loading_boss, game_data)
            for player in fight.players:
                loaders.append(PlayerLoader(player, game_data=game_data))

        loaders = [loader for loader in loaders if loader.needs_load()]
        try:
            if loaders:
                await asyncio.gather(*[loader.load(client=client) for loader in loaders])
            else:
                await client.query(f'reportData {{ report(code: "{report.report_id}") {{ code }} }}')
        except (PrivateReportError, UnknownReportError):
            logger.warning("Skipping report %s during spec ranking refresh", report.report_id)
            return report.report_id

        for fight in fights_ready_for_phase_correction(fights_loading_phases, fights_loading_boss):
            correct_loaded_phases(fight, game_data)
        return None
