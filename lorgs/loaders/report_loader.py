from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import asyncio
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.loaders.fight_loader import FightLoader
from lorgs.loaders.player_loader import PlayerLoader
from lorgs.loaders.report_overview_loader import ReportOverviewLoader


if typing.TYPE_CHECKING:
    from lorgs.clients.wcl.client import WarcraftlogsClient
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
    async def _load_fights(
        self,
        client: WarcraftlogsClient | None = None,
        fight_ids: list[int] = [],  # noqa: B006
    ) -> None:
        """Load the fights for the report."""
        fights = self.report.get_fights(*fight_ids)
        loaders = [FightLoader(fight=fight) for fight in fights]
        loaders = [loader for loader in loaders if loader.needs_load()]
        await asyncio.gather(*[loader.load(client=client) for loader in loaders])

    async def _load_players(
        self,
        client: WarcraftlogsClient | None = None,
        fight_ids: list[int] = [],  # noqa: B006
        player_ids: list[int] = [],  # noqa: B006
    ) -> None:
        """Load the players for the report."""
        players = []
        for fight in self.report.get_fights(*fight_ids):
            players.extend(fight.get_players(*player_ids))

        loaders = [PlayerLoader(player) for player in players]
        loaders = [loader for loader in loaders if loader.needs_load()]
        await asyncio.gather(*[loader.load(client=client) for loader in loaders])

    async def load(
        self,
        client: WarcraftlogsClient | None = None,
        fight_ids: list[int] | None = None,
        player_ids: list[int] | None = None,
    ) -> None:
        fight_ids = fight_ids or []
        player_ids = player_ids or []

        # load the report overview if not already loaded
        if not self.report.fights:
            overview_loader = ReportOverviewLoader(report=self.report)
            await overview_loader.load(client=client)

        # load the fights
        await self._load_fights(client=client, fight_ids=fight_ids)

        # load the players
        await self._load_players(client=client, fight_ids=fight_ids, player_ids=player_ids)
