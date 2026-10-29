from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import textwrap
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.clients import wcl
from lorgs.data import get_game_version_by_wcl_id
from lorgs.loaders.fight_loader import FightLoader
from lorgs.logger import logger
from lorgs.models.warcraftlogs_player import Player
from lorgs.models.warcraftlogs_report import Report

from .base_loader import BaseLoader


if typing.TYPE_CHECKING:
    from lorgs.models.game_data import GameData


class UnsupportedGameVersionError(ValueError):
    """The log belongs to a Warcraft Logs game version that none of our Game Versions serves."""

    def __init__(self, wcl_game_version: int) -> None:
        super().__init__(f"Unsupported Warcraft Logs game version: {wcl_game_version}")
        self.wcl_game_version = wcl_game_version


class ReportOverviewLoader(BaseLoader):
    """Loads the Overview of a Report.

    Without `game_data` the Game Version is picked from the log's Warcraft Logs `masterData.gameVersion`.
    """

    def __init__(self, report: Report, game_data: GameData | None = None) -> None:
        # Optional until the log's Warcraft Logs game version is known.
        super().__init__(game_data)  # ty: ignore[invalid-argument-type]
        self.report = report

    def get_query(self):
        """Get the Query to load this Reports Overview."""
        return textwrap.dedent(
            f"""
        reportData
        {{
            report(code: "{self.report.report_id}")
            {{
                title
                zone {{name id}}
                startTime

                owner {{ name }}

                guild {{
                    name
                    server {{ name }}
                }}

                masterData
                {{
                    gameVersion
                    actors(type: "Player")
                    {{
                        name
                        id
                        subType
                        icon    # the icon includes the spec name
                    }}
                }}

                fights
                {{
                    id
                    encounterID
                    startTime
                    endTime
                    fightPercentage
                    kill
                    difficulty

                    phaseTransitions {{
                        id
                        startTime
                    }}
                }}
            }}
        }}
        """,
        )

    def _player_from_actor_data(self, actor_data: wcl.ReportActor) -> Player | None:
        if actor_data.type != "Player":
            return None

        # guess spec from the icon
        # WCL gives us an icon matching the spec, IF a player
        # played the same spec in all fights inside a report.
        # Otherwise it only includes a class-name.
        # TODO: this has been fixed recently. there should be a new array of specs now.
        icon_name = actor_data.icon
        spec_slug = icon_name.lower() if "-" in icon_name else ""

        player_class = self.game_data.get_class(actor_data.subType.lower())
        if player_class is None:
            logger.debug("Skipping unknown Player: %s", actor_data.name)
            return None

        # create the new player
        return Player(
            source_id=actor_data.id,
            name=actor_data.name,
            class_slug=player_class.name_slug,
            spec_slug=spec_slug,
        )

    def _process_master_data(self, master_data: wcl.ReportMasterData) -> None:
        """Create the Players from the passed Report-MasterData."""
        self.report.game_version = master_data.gameVersion

        # clear out any old instances
        # print("master_data", master_data)
        self.report.players = []
        for actor_data in master_data.actors:
            if player := self._player_from_actor_data(actor_data):
                self.report.players.append(player)

    def _process_fights(self, fights: list[wcl.ReportFight]) -> None:
        """Create the Fights from the passed Report-Fights."""
        for fight_data in fights:
            if self.report.get_fight(fight_data.id):
                continue  # already loaded

            if fight := FightLoader.fight_from_wcl_fight(fight_data, report=self.report, game_data=self.game_data):
                fight.report = self.report
                self.report.fights.append(fight)

        # make pydantic believe the list has changed
        self.report.fights = self.report.fights[:]

    def process_query_result(self, query_result: dict[str, typing.Any]) -> None:
        report_data = wcl.ReportData(**query_result)
        report = report_data.report

        if self.game_data is None:
            wcl_game_version = report.masterData.gameVersion if report.masterData else 1
            game_version = get_game_version_by_wcl_id(wcl_game_version)
            if game_version is None:
                raise UnsupportedGameVersionError(wcl_game_version)
            self.game_data = game_version.data

        # Update the Report itself
        self.report.title = report.title
        self.report.start_time = report.startTime
        self.report.zone_id = report.zone.id
        self.report.owner = report.owner.name

        guild = report.guild
        self.report.guild = guild.name if guild else ""

        if report.masterData:
            self._process_master_data(report.masterData)

        if report.fights:
            self._process_fights(report.fights)
