from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import asyncio
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.loaders.boss_loader import BossLoader
from lorgs.loaders.fight_loader import FightLoader
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
        # TODO: might have to compare this to the requested fight ids
        if not self.report.fights:
            overview_loader = ReportOverviewLoader(report=self.report)
            await overview_loader.load(client=client)

        loaders: list[BaseLoader] = []
        for fight_id in fight_ids:

            fight = self.report.get_fight(fight_id)
            if not fight:
                # ReportOverviewLoader should have loaded the fight
                # this must be an invalid ID or a bug
                logger.error(f"Fight {fight_id} not found in report")
                continue

            # make sure the fight overview is loaded
            # we can't use the ReportOverview since player specs might be
            # different from fight to fight
            if not fight.players:
                await FightLoader(fight=fight).load(client=client)

            # boss
            if load_boss and fight.boss:
                loaders.append(BossLoader(fight.boss))

            # players
            for player_id in player_ids:
                player = fight.get_player(source_id=player_id)
                if not player:
                    # could be a player thats benched on this fight,
                    # on a multi-select load
                    continue

                loaders.append(PlayerLoader(player))

        loaders = [loader for loader in loaders if loader.needs_load()]
        logger.info(f"load {len(loaders)} items")
        if loaders:
            await asyncio.gather(*[loader.load(client=client) for loader in loaders])
