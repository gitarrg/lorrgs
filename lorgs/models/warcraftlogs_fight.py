from __future__ import annotations

# IMPORT STANRD LIBRARIES
import datetime
import textwrap
import typing
from typing import Optional

# IMPORT THIRD PARTY LIBRARIES
import pydantic

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.clients import wcl
from lorgs.logger import logger
from lorgs.models import warcraftlogs_base
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
    boss: Optional[Boss] = None
    phases: list[Phase] = []

    deaths: int = 0
    damage_taken: int = 0

    percent: float = 0
    """boss percentage at the end of the fight."""
    kill: bool = True

    report: typing.Optional["Report"] = pydantic.Field(default=None, exclude=True)

    def post_init(self) -> None:
        actors = self.players + [self.boss]
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

    def add_phase(self, ts: int, name: str, mrt: str = "") -> Phase:
        """Add a new phase to the fight."""

        if not self.phases:
            self.phases = []  # force new list to trick pydantics "excludeUnset"

        name = name.format(len(self.phases) + 1)
        phase = Phase(ts=ts, name=name, mrt=mrt)
        self.phases.append(phase)
        return phase

    ############################################################################
    # Query
    #
    @property
    def table_query_args(self) -> str:
        return f"fightIDs: {self.fight_id}, startTime: {self.start_time_rel}, endTime: {self.end_time_rel}"

    ############################################################################
    #   Summary
    #
    def get_query_parts(self) -> list[str]:
        return [f"summary: table({self.table_query_args}, dataType: Summary)"]

    def get_query(self) -> str:
        """Get the Query to load the fights summary."""
        if self.players:
            logger.info("no players")
            return ""

        if not self.report:
            raise ValueError("Missing Parent Report")

        parts = "\n".join(self.get_query_parts())

        return textwrap.dedent(
            f"""\
            reportData
            {{
                report(code: "{self.report.report_id}")
                {{
                    {parts}
                }}
            }}
        """
        )

    def process_players(self, summary_data: "wcl.ReportSummary"):
        total_damage = summary_data.damageDone
        total_healing = summary_data.healingDone

        for composition_data in summary_data.composition:
            # Get Class and Spec
            if not composition_data.specs:
                logger.warning("Player has no spec: %s", composition_data.name)
                continue

            spec_data = composition_data.specs[0]
            spec_name = spec_data.spec
            class_name = composition_data.type
            spec = WowSpec.get(name_slug_cap=spec_name, wow_class__name_slug_cap=class_name)
            if not spec:
                logger.warning("Unknown Spec: %s", spec_name)
                continue

            # Get Total Damage or Healing
            total_data = total_healing if spec.role.code == "heal" else total_damage
            for data in total_data:
                if data.id == composition_data.id:
                    total = data.total / (self.duration / 1000)
                    break
            else:
                total = 0

            # create and return yield player object
            player = Player(
                source_id=composition_data.id,
                name=composition_data.name,
                class_slug=spec.wow_class.name_slug,
                spec_slug=spec.full_name_slug,
                total=int(total),
            )
            player.fight = self
            player.process_death_events(summary_data.deathEvents)
            self.players.append(player)

        self.players.sort(key=lambda player: (player.spec.role, player.spec, player.name))

    def process_query_result(self, **query_result: typing.Any):
        """Process the data retured from an Overview-Query."""
        report_data = wcl.ReportData(**query_result)
        if not report_data.report.summary:
            return
        summary_data = report_data.report.summary
        self.duration = self.duration or summary_data.totalTime
        self.process_players(summary_data)

        for player in self.players:
            player.process_query_result(**query_result)

    ############################################################################
    #   Load Player:
    #
    async def load_actors(self, player_ids: typing.Optional[list[int]] = None):
        player_ids = player_ids or []

        if not self.players:
            await self.load()

        # Get Players to load
        actors_to_load: list["BaseActor"] = []
        actors_to_load += self.get_players(*player_ids)
        actors_to_load += [self.boss] if self.boss else []
        actors_to_load = [actor for actor in actors_to_load if not actor.casts]
        if not actors_to_load:
            return

        # load
        await self.load_many(actors_to_load)  # type: ignore

        # Create a new list (otherwise pydantic would consider it as unset )
        self.players = [p for p in self.players]
