from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.loaders.fights_loader import FightFailure, FightPlan, load_fights
from lorgs.loaders.report_overview_loader import ReportOverviewLoader
from lorgs.logger import logger


if typing.TYPE_CHECKING:
    from lorgs.clients.wcl.client import WarcraftlogsClient
    from lorgs.models.game_data import GameData
    from lorgs.models.warcraftlogs_report import Report


class ReportLoader:
    """Loads a Report's overview and the Fights picked from it. The Fights themselves are loaded by `load_fights`."""

    def __init__(self, report: Report, game_data: GameData) -> None:
        self.report = report
        self.game_data = game_data

    async def load(
        self,
        client: WarcraftlogsClient | None = None,
        fight_ids: list[int] | None = None,
        player_ids: list[int] | None = None,
        *,
        load_boss: bool = False,
    ) -> list[FightFailure]:
        """Load the overview if missing, then the picked Fights. Returns the Fights that failed."""
        if not self.report.fights:
            await ReportOverviewLoader(
                report=self.report,
                game_data=self.game_data,
            ).load(client=client)

        plans: list[FightPlan] = []
        for fight_id in fight_ids or []:
            fight = self.report.get_fight(fight_id)
            if not fight:
                # invalid id or a bug: the overview should have loaded every Fight
                logger.error(f"Fight {fight_id} not found in report")
                continue
            plan = FightPlan(fight=fight, players=player_ids or None, boss=load_boss)
            plans.append(plan)

        logger.info(f"load {len(plans)} fights")
        return await load_fights(plans, self.game_data, client=client)
