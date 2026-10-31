"""Models represeting the Data we recive from WCL under the worldData.encounter.fightRankings."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import datetime

# IMPORT THIRD PARTY LIBRARIES
from pydantic import BaseModel

# IMPORT LOCAL LIBRARIES
from .guild import Guild


class FightRankingsItemsReport(BaseModel):
    code: str = ""
    """Report Code"""

    fightID: int = 0

    startTime: datetime.datetime = datetime.datetime.fromtimestamp(0, datetime.UTC)
    """Report Start Time."""


class FightRankingsFight(BaseModel):
    """A Single Fight from the Encounter Fight Rankings."""

    # code: str
    """ID of the Report. eg.: tZVAxLYg7kTz1PBm"""

    # fightID: int
    """ID of the Fight."""

    # TODO: add "Server" Class
    # server: Server = None

    duration: int = 0
    """Fight Duration in Milliseconds."""

    startTime: datetime.datetime = datetime.datetime.fromtimestamp(0, datetime.UTC)
    """Fight Start Time in Milliseconds."""

    guild: Guild | None = None

    report: FightRankingsItemsReport = FightRankingsItemsReport()
    """Parent Report Info."""

    damageTaken: int = 0
    deaths: int = 0

    tanks: int = 0
    healers: int = 0
    melee: int = 0
    ranged: int = 0

    bracketData: float = 0
    """A specific bracket (e.g., item level range) to use instead of overall rankings. For WoW, brackets are item levels or keystones. For FF, brackets are patches."""


class FightRankings(BaseModel):
    ###################
    # Query

    bracket: int = 0
    """A specific bracket (e.g., item level range) to use instead of overall rankings.
    For WoW, brackets are item levels or keystone"""

    difficulty: int = 0
    """A specific difficulty to fetch rankings for.
    If omitted, the highest difficulty is used."""

    filter: str = ""
    """A filter string for advanced searching.
    The syntax matches the one used on the web site exactly,
    so you can filter encounter rankings on the site to figure out the string to use."""

    page: int = 1
    """Which page of rankings to fetch. By default the first page is used."""

    partition: int = 0
    """Whether or not to filter the rankings to a specific partition.
    By default, the latest partition is chosen."""

    serverRegion: str = ""
    """The short name of a region to filter to.
    If paired with a server slug, will uniquely identify a server.
    If used by itself, rankings for that specific region will be fetched."""

    serverSlug: str = ""
    """The slug for a specific server. Whether or not to filter rankings to a specific server.
    If omitted, data for all servers will be used."""

    size: int = 0
    """Whether or not to filter rankings to a specific size.
    If omitted, the first valid raid size will be used."""

    metric: str = ""
    """You can filter to a specific fight metric like speed or execution. If omitted, an appropriate default fight metric for the zone will be chosen."""

    ###################
    # Results

    hasMorePages: bool = False

    count: int = 0

    rankings: list[FightRankingsFight] = []
