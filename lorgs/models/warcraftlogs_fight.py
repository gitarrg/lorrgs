from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import asyncio
import datetime
import textwrap
import typing

# IMPORT THIRD PARTY LIBRARIES
import pydantic

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.clients import wcl
from lorgs.logger import logger
from lorgs.models import warcraftlogs_base
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.warcraftlogs_boss import Boss
from lorgs.models.warcraftlogs_player import Player
from lorgs.models.wow_spec import WowSpec


if typing.TYPE_CHECKING:
    from lorgs.models.warcraftlogs_actor import BaseActor
    from lorgs.models.warcraftlogs_report import Report


class Phase(pydantic.BaseModel):
    """A phase within a Fight."""

    timestamp: int = pydantic.Field(alias="ts")
    name: str = "Phase"
    mrt: str = ""


class Fight(warcraftlogs_base.BaseModel):
    fight_id: int

    start_time: datetime.datetime
    """Encounter Start."""

    duration: int = 0
    """fight duration in milliseconds."""

    players: list[Player] = []
    boss: Boss | None = None
    phases: list[Phase] = []

    deaths: int = 0
    damage_taken: int = 0

    percent: float = 0
    """boss percentage at the end of the fight."""
    kill: bool = True

    difficulty: RaidDifficulty = RaidDifficulty.UNKNOWN

    _report: Report | None = None

    @property
    def report(self) -> Report | None:
        """Parent report (private storage to avoid Pydantic schema resolution)."""
        return self._report

    @report.setter
    def report(self, value: Report | None) -> None:
        self._report = value

    def post_init(self) -> None:
        actors = [*self.players, self.boss]
        for actor in actors:
            if actor:
                actor.fight = self

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.fight_id}, players={len(self.players)})"

    def summary(self) -> dict[str, typing.Any]:
        raid_boss_name = self.boss and self.boss.raid_boss and self.boss.raid_boss.full_name_slug

        return {
            # required for spec rankings
            "report_id": self.report and self.report.report_id or "",
            "fight_id": self.fight_id,
            "percent": self.percent,
            "kill": self.kill,
            "duration": self.duration,
            "time": self.start_time.isoformat(),
            "boss": {"name": raid_boss_name},
            "difficulty": self.difficulty.value,
        }

    def as_dict(self, player_ids: list[int] = []) -> dict:
        # Get players
        players = self.players
        if player_ids:
            players = [player for player in players if player.source_id in player_ids]
        players = sorted(players, key=lambda player: (player.spec.role, player.spec, player.name))

        # Return
        return {
            **self.summary(),
            "players": [player.as_dict() for player in players],
            "boss": self.boss.as_dict() if self.boss else {},
        }

    ##########################
    # Attributes
    @property
    def end_time(self) -> datetime.datetime:
        return self.start_time + datetime.timedelta(milliseconds=self.duration)

    @property
    def start_time_rel(self) -> int:
        """Fight start time, relative the parent report (in milliseconds)."""
        t = self.report.start_time.timestamp() if self.report else 0
        return int(1000 * (self.start_time.timestamp() - t))

    @property
    def end_time_rel(self) -> int:
        """fight end time, relative to the report (in milliseconds)."""
        t = self.report.start_time.timestamp() if self.report else 0
        return int(1000 * (self.end_time.timestamp() - t))

    #################################
    # Methods
    #
    def get_player(self, **kwargs) -> typing.Optional[Player]:
        """Returns a single Player based on the kwargs."""
        return utils.get(self.players, **kwargs)

    def get_players(self, *source_ids: int) -> list[Player]:
        """Gets multiple players based on source id."""
        players = self.players
        if source_ids:
            players = [player for player in players if player.source_id in source_ids]

        return [player for player in players if player]

    def add_phase(self, ts: int) -> Phase:
        """Add a new phase to the fight."""

        if not self.phases:
            self.phases = []  # force new list to trick pydantics "excludeUnset"

        phase = Phase(ts=ts)
        self.phases.append(phase)
        return phase

    ############################################################################
    # Query
    #
    @property
    def table_query_args(self) -> str:
        return f"fightIDs: {self.fight_id}, startTime: {self.start_time_rel}, endTime: {self.end_time_rel}"

    ############################################################################
    #   Load actors (uses new loaders for actor data)
    #
    async def load_actors(self, player_ids: list[int] | None = None):
        raise NotImplementedError("use loaders instead")

        player_ids = player_ids or []

        if not self.players:
            await self.load()

        actors_to_load: list[BaseActor] = []
        actors_to_load += self.get_players(*player_ids)
        actors_to_load += [self.boss] if self.boss else []
        actors_to_load = [actor for actor in actors_to_load if not actor.casts]
        if not actors_to_load:
            return

        client = self.client
        tasks = [loader_for(actor).load(client, raise_errors=False) for actor in actors_to_load]
        await asyncio.gather(*tasks)

        # Create a new list (otherwise pydantic would consider it as unset )
        self.players = [p for p in self.players]
