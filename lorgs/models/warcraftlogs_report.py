"""Class and Functions to manage Report-Instances."""

from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
import asyncio

# IMPORT STANDARD LIBRARIES
import datetime
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.models import warcraftlogs_base
from lorgs.models.warcraftlogs_fight import Fight  # noqa: TC001  # required by pydantic
from lorgs.models.warcraftlogs_player import Player  # noqa: TC001  # required by pydantic


class Report(warcraftlogs_base.BaseModel):
    """Defines a Report read from WarcraftLogs.com and stores in our DB."""

    report_id: str
    """16 digit unique id/code as used on warcraftlogs."""

    start_time: datetime.datetime = datetime.datetime.min
    """time the report itself has started. The first fight might start later."""

    title: str = ""
    """title of the report."""

    zone_id: int = 0

    guild: str = ""
    """The guild that the report belongs to. None if it was a logged as a personal report."""

    region: str = ""
    """Realm Region of the Report. (eg.: "US", "EU", "KR", "TW")"""

    owner: str = ""
    """The user that uploaded the report."""

    fights: list[Fight] = []
    """fights in this report keyed by fight_id. (they may or may not be loaded)."""

    players: list[Player] = []
    """players in this report.
    Note: not every player might participate in every fight."""

    def post_init(self) -> None:
        for fight in self.fights:
            fight.report = self
            fight.post_init()

    def __str__(self) -> str:
        return f"<Report({self.report_id}, num_fights={len(self.fights)})>"

    ##########################
    # Attributes
    #
    def as_dict(self) -> dict[str, typing.Any]:
        """Return a Summary/Overview about this report."""
        info = {
            "title": self.title,
            "report_id": self.report_id,
            "date": int(self.start_time.timestamp()),
            "zone_id": self.zone_id,
            "guild": self.guild,
            "owner": self.owner,
        }

        # for players and fights we only include essential data
        info["fights"] = {fight.fight_id: fight.summary() for fight in self.fights}
        info["players"] = {player.source_id: player.summary() for player in self.players}
        return info

    ##########################
    # Methods
    #
    def get_fight(self, fight_id: int) -> Fight | None:
        """Get a single fight from this Report."""
        for fight in self.fights:
            if fight.fight_id == fight_id:
                return fight
        return None

    def get_fights(self, *fight_ids: int) -> list[Fight]:
        """Get a multiple fights based of their fight ids."""
        fights = [self.get_fight(fight_id) for fight_id in fight_ids]
        return [f for f in fights if f]

    ############################################################################
    # Query
    #
    async def load_fight(self, fight_id: int, player_ids: list[int]):
        """Load a single Fight from this Report."""
        fight = self.get_fight(fight_id=fight_id)
        if not fight:
            raise ValueError("invalid fight id")

        await fight.load_actors(player_ids=player_ids)

    async def load_fights(self, fight_ids: list[int], player_ids: list[int]) -> None:
        if not self.fights:
            await self.load()

        # queue all tasks at once.
        # the client will make sure its throttled accordingly
        tasks = [self.load_fight(fight_id=fight_id, player_ids=player_ids) for fight_id in fight_ids]
        await asyncio.gather(*tasks)
