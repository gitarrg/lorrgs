"""Class and Functions to manage Report-Instances."""

from __future__ import annotations

# IMPORT STANRD LIBRARIES
import asyncio
import datetime
import textwrap
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.clients import wcl
from lorgs.logger import logger
from lorgs.models import warcraftlogs_base
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.warcraftlogs_boss import Boss
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_player import Player


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
        return f"<BaseReport({self.report_id}, num_fights={len(self.fights)})>"

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
    def add_fight(self, fight_data: wcl.ReportFight):
        """Add a new Fight to this Report."""
        # skip trash fights
        if not fight_data.encounterID:
            return

        fight = Fight(
            fight_id=fight_data.id,
            percent=fight_data.fightPercentage,
            kill=fight_data.kill,
            start_time=self.start_time + datetime.timedelta(milliseconds=fight_data.startTime),
            duration=fight_data.endTime - fight_data.startTime + 1,  # somehow there is 1ms missing
        )
        fight.report = self  # TODO: replace in favor of `post_init()``

        # Fight: Boss
        raid_boss = RaidBoss.get(id=fight_data.encounterID)
        if raid_boss:
            fight.boss = Boss.from_raid_boss(raid_boss)
            fight.boss.fight = fight

        # store and return
        self.fights.append(fight)
        return fight

    def get_fight(self, fight_id: int):
        """Get a single fight from this Report."""
        for fight in self.fights:
            if fight.fight_id == fight_id:
                return fight

    def get_fights(self, *fight_ids: int) -> list[Fight]:
        """Get a multiple fights based of their fight ids."""
        fights = [self.get_fight(fight_id) for fight_id in fight_ids]
        return [f for f in fights if f]

    def add_player(self, actor_data: wcl.ReportActor):
        if actor_data.type != "Player":
            return

        # guess spec from the icon
        # WCL gives us an icon matching the spec, IF a player
        # played the same spec in all fights inside a report.
        # Otherwise it only includes a class-name.
        icon_name = actor_data.icon
        spec_slug = icon_name.lower() if "-" in icon_name else ""

        # create the new player
        player = Player(
            source_id=actor_data.id,
            name=actor_data.name,
            class_slug=actor_data.subType.lower(),
            spec_slug=spec_slug,
        )

        if player.class_ == None:
            logger.debug("Skipping unknown Player: %s", player)
            return

        # add to to the report
        self.players.append(player)

    ############################################################################
    # Query
    #
    def get_query(self):
        """Get the Query to load this Reports Overview."""
        return textwrap.dedent(
            f"""
        reportData
        {{
            report(code: "{self.report_id}")
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
                }}
            }}
        }}
        """
        )

    def process_master_data(self, master_data: wcl.ReportMasterData) -> None:
        """Create the Players from the passed Report-MasterData"""
        # clear out any old instances
        self.players = []
        for actor_data in master_data.actors:
            self.add_player(actor_data)

    def process_report_fights(self, fights: list[wcl.ReportFight]) -> None:
        """Update the Fights in this report."""
        # clear out any old data
        self.fights = []
        for fight in fights:
            self.add_fight(fight)

    def process_query_result(self, **query_result: typing.Any):
        report_data = wcl.ReportData(**query_result)
        report = report_data.report

        # Update the Report itself
        self.title = report.title
        self.start_time = report.startTime
        self.zone_id = report.zone.id
        self.owner = report.owner.name

        guild = report.guild
        self.guild = guild.name if guild else ""

        if report.masterData:
            self.process_master_data(report.masterData)
        self.process_report_fights(report.fights)

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
