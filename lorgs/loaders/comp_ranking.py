"""Loader for CompRanking data from WarcraftLogs."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import datetime
import textwrap
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.models.warcraftlogs_boss import Boss
from lorgs.models.warcraftlogs_comp_ranking import CompRankingFight, CompRankingReport

from .base_loader import BaseLoader


if typing.TYPE_CHECKING:
    from lorgs.clients import wcl
    from lorgs.models.game_version import GameVersion
    from lorgs.models.warcraftlogs_comp_ranking import CompRanking


class CompRankingLoader(BaseLoader):
    """Loads the fight rankings page of a boss into a CompRanking.

    Only the ranking page is fetched, no fight events.
    """

    metric = "execution"
    """Ranking metric to query."""

    def __init__(
        self,
        ranking: CompRanking,
        game_version: GameVersion,
        *,
        page: int = 1,
        clear_old: bool = False,
    ) -> None:
        if ranking.game_version != game_version.name:
            msg = f"Ranking belongs to Game Version {ranking.game_version!r}, not {game_version.name!r}"
            raise ValueError(msg)
        super().__init__(game_version.data)
        self.ranking = ranking
        self.page = page
        self.clear_old = clear_old

    def get_query(self) -> str:
        boss = self.game_data.get_boss(full_name_slug=self.ranking.boss_slug)
        if not boss:
            raise ValueError(f"Unknown Boss: {self.ranking.boss_slug}")

        return textwrap.dedent(
            f"""
            worldData
            {{
                encounter(id: {boss.id})
                {{
                    fightRankings(
                        metric: {self.metric}
                        page: {self.page}
                    )
                }}
            }}
            """,
        )

    def add_report(self, fight_data: wcl.FightRankingsFight) -> None:
        """Add a new Report/Fight to the Ranking."""
        fight = CompRankingFight(
            fight_id=fight_data.report.fightID,
            start_time=fight_data.startTime,
            duration=fight_data.duration,
            boss=Boss(boss_slug=self.ranking.boss_slug),
            players=[],
            damage_taken=fight_data.damageTaken,
            deaths=fight_data.deaths,
        )
        report = CompRankingReport(
            report_id=fight_data.report.code,
            start_time=fight_data.report.startTime,
            fights=[fight],
        )
        self.ranking.reports.append(report)

    def process_query_result(self, query: wcl.Query) -> None:
        ranking = self.ranking

        # copy the list, to make pydantic believe it has changed
        ranking.reports = [] if self.clear_old else ranking.reports[:]
        known = {(report.report_id, fight.fight_id) for report in ranking.reports for fight in report.fights}

        for fight_data in query.world_data.encounter.fightRankings.rankings:
            if (fight_data.report.code, fight_data.report.fightID) not in known:
                self.add_report(fight_data)

        ranking.sort_reports()
        ranking.updated = datetime.datetime.now(datetime.UTC)
