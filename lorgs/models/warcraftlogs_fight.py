from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import datetime
import typing

# IMPORT THIRD PARTY LIBRARIES
import blinker
import pydantic

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.warcraftlogs_boss import Boss  # ruff: ignore[typing-only-first-party-import] # required by pydantic
from lorgs.models.warcraftlogs_player import Player  # ruff: ignore[typing-only-first-party-import] # required by pydantic


if typing.TYPE_CHECKING:
    from lorgs.models.game_data import GameData
    from lorgs.models.warcraftlogs_report import Report


class Phase(pydantic.BaseModel):
    """A phase within a Fight."""

    timestamp: int = pydantic.Field(alias="ts")
    name: str = "Phase"
    mrt: str = ""
    phase_id: int | float = 0


class Fight(base.BaseModel):
    fight_id: int

    start_time: base.UTCDatetime
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

    event_fight_load: typing.ClassVar[blinker.Signal] = blinker.signal("fight.load")
    event_fight_phases_load: typing.ClassVar[blinker.Signal] = blinker.signal("fight.phases.load")

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
        raid_boss_name = self.boss and self.boss.boss_slug

        return {
            # required for spec rankings
            "report_id": (self.report and self.report.report_id) or "",
            "fight_id": self.fight_id,
            "percent": self.percent,
            "kill": self.kill,
            "duration": self.duration,
            "time": self.start_time.isoformat(),
            "boss": {"name": raid_boss_name},
            "difficulty": self.difficulty.value,
        }

    @staticmethod
    def _sort_key(player: Player, game_data: GameData) -> tuple:
        if spec := game_data.get_spec(player.spec_slug):
            return (spec.role, spec, player.name)
        return (None, None, player.name)

    def as_dict(self, game_data: GameData, player_ids: list[int] = []) -> dict:
        # Get players
        players = self.players
        if player_ids:
            players = [player for player in players if player.source_id in player_ids]
        players = sorted(players, key=lambda player: self._sort_key(player, game_data))

        # Return
        return {
            **self.summary(),
            "players": [player.as_dict(game_data) for player in players],
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
        """Fight end time, relative to the report (in milliseconds)."""
        t = self.report.start_time.timestamp() if self.report else 0
        return int(1000 * (self.end_time.timestamp() - t))

    def to_fight_time(self, report_time: int) -> int:
        """Convert a Warcraft Logs report timestamp into milliseconds since the fight started."""
        if not self.report:
            raise ValueError("Missing Parent Report")
        return report_time - self.start_time_rel

    #################################
    # Methods
    #
    def get_player(self, *, get_from_report: bool = False, **kwargs) -> Player | None:
        """Returns a single Player based on the kwargs."""
        if player := utils.get(self.players, **kwargs):
            return player

        if get_from_report and self.report:
            report_player = self.report.get_player(**kwargs)
            if not report_player:
                return None
            player = report_player.model_copy()
            player.fight = self
            self.players.append(player)
            self.players = self.players[:]  # force pydantic to update the list
            return player

        return None

    def get_players(self, *source_ids: int) -> list[Player]:
        """Gets multiple players based on source id."""
        players = self.players
        if source_ids:
            players = [player for player in players if player.source_id in source_ids]
        return players

    def add_phase(self, phase: Phase | None = None, **kwargs: typing.Any) -> Phase:
        """Add a new phase to the fight."""
        if not self.phases:
            self.phases = []  # force new list to trick pydantics "excludeUnset"

        if not phase:
            phase = Phase(**kwargs)

        # auto enumerate phases
        if not phase.phase_id:
            # pull is "P1", first real phase is P2
            phase.phase_id = len(self.phases) + 2

        self.phases.append(phase)
        return phase

    def remove_empty_players(self) -> None:
        """Remove empty players from the fight."""
        self.players = [player for player in self.players if player.casts]

    ############################################################################
    # Query
    #
    @property
    def table_query_args(self) -> str:
        return f"fightIDs: {self.fight_id}, startTime: {self.start_time_rel}, endTime: {self.end_time_rel}"
