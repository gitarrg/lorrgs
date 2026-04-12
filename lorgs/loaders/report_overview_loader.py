from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import textwrap
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.clients import wcl
from lorgs.loaders.fight_loader import FightLoader
from lorgs.logger import logger
from lorgs.models.warcraftlogs_player import Player
from lorgs.models.warcraftlogs_report import Report
from lorgs.models.wow_class import WowClass

from .base_loader import BaseLoader


class ReportOverviewLoader(BaseLoader):
    def __init__(self, report: Report) -> None:
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

        player_class = WowClass.get(name_slug=actor_data.subType.lower())
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
        # clear out any old instances
        # print("master_data", master_data)
        self.report.players = []
        for actor_data in master_data.actors:
            if player := self._player_from_actor_data(actor_data):
                self.report.players.append(player)

    def _process_fights(self, fights: list[wcl.ReportFight]) -> None:
        """Create the Fights from the passed Report-Fights."""
        self.report.fights = []  # clear out any old instances

        for fight_data in fights:
            if fight := FightLoader.fight_from_wcl_fight(fight_data, report=self.report):
                fight.report = self.report
                self.report.fights.append(fight)

    def process_query_result(self, query_result: dict[str, typing.Any]) -> None:
        report_data = wcl.ReportData(**query_result)
        report = report_data.report

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
