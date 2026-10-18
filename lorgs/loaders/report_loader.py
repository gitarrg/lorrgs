from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import asyncio
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.loaders.fight_loader import FightLoader
from lorgs.loaders.fight_phases import (
    FightPhasesLoader,
    correct_loaded_phases,
    fights_ready_for_phase_correction,
    queue_boss_loader,
)
from lorgs.loaders.player_loader import PlayerLoader
from lorgs.loaders.report_overview_loader import ReportOverviewLoader
from lorgs.logger import logger


if typing.TYPE_CHECKING:
    from lorgs.clients.wcl.client import WarcraftlogsClient
    from lorgs.loaders.base_loader import BaseLoader
    from lorgs.models.warcraftlogs_fight import Fight
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

        loaders, fights_loading_phases, fights_loading_boss = await self._collect_loaders(
            client,
            fight_ids,
            player_ids,
            load_boss=load_boss,
        )
        loaders = [loader for loader in loaders if loader.needs_load()]
        logger.info(f"load {len(loaders)} items")
        if loaders:
            await asyncio.gather(*[loader.load(client=client) for loader in loaders])

        ready = fights_ready_for_phase_correction(fights_loading_phases, fights_loading_boss)
        for fight in ready:
            correct_loaded_phases(fight)

    async def _collect_loaders(
        self,
        client: WarcraftlogsClient | None,
        fight_ids: list[int],
        player_ids: list[int],
        *,
        load_boss: bool,
    ) -> tuple[list[BaseLoader], list[Fight], list[Fight]]:
        loaders: list[BaseLoader] = []
        fights_loading_phases: list[Fight] = []
        fights_loading_boss: list[Fight] = []
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
                phases_need_load = FightPhasesLoader(fight).needs_load()
                await FightLoader(fight=fight).load(client=client)
                if phases_need_load:
                    fights_loading_phases.append(fight)

            # boss
            if load_boss:
                queue_boss_loader(fight, loaders, fights_loading_boss)

            # players
            for player_id in player_ids:
                player = fight.get_player(source_id=player_id)
                if not player:
                    # could be a player thats benched on this fight,
                    # on a multi-select load
                    continue

                loaders.append(PlayerLoader(player))

        return loaders, fights_loading_phases, fights_loading_boss
