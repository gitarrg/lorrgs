from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import asyncio
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.loaders.boss_loader import BossLoader
from lorgs.loaders.fight_phases import FightPhasesLoader
from lorgs.loaders.player_loader import PlayerLoader
from lorgs.loaders.report_overview_loader import ReportOverviewLoader
from lorgs.logger import logger


if typing.TYPE_CHECKING:
    from lorgs.clients.wcl.client import WarcraftlogsClient
    from lorgs.loaders.base_loader import BaseLoader
    from lorgs.models.warcraftlogs_report import Report


class ReportLoader:
    """Loader for Report instances.

    Note: this behaves similar to a BaseLoader, but is not a subclass of it.
    since all the logic is delegated to the other loaders.
    In the future we might inherit from BaseLoader, but for now it's not really necessary.
    """

    def __init__(self, report: Report) -> None:
        self.report = report

    ############################################################################
    # Load
    #
    async def load(
        self,
        client: WarcraftlogsClient | None = None,
        fight_ids: list[int] | None = None,
        player_ids: list[int] | None = None,
        *,
        load_boss: bool = False,
    ) -> None:
        fight_ids = fight_ids or []
        player_ids = player_ids or []

        # load the report overview if not already loaded
        if not self.report.fights:
            overview_loader = ReportOverviewLoader(report=self.report)
            await overview_loader.load(client=client)


        loaders: list[BaseLoader] = []
        # load boss and players
        #
        for fight in self.report.get_fights(*fight_ids):

            # fight
            loaders.append(FightPhasesLoader(fight=fight))

            # boss
            if load_boss and fight.boss:
                loaders.append(BossLoader(fight.boss))

            # players
            for player in fight.get_players(*player_ids):
                loaders.append(PlayerLoader(player))

        loaders = [loader for loader in loaders if loader.needs_load()]
        logger.info(f"load {len(loaders)} items")
        if loaders:
            await asyncio.gather(*[loader.load(client=client) for loader in loaders])
