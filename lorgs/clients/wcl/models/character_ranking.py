"""Models represeting the Data we recive from WCL under the worldData.encounter.charaterRankings."""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import datetime

# IMPORT THIRD PARTY LIBRARIES
from pydantic import BaseModel, Field


class CharacterRankingReportFightData(BaseModel):
    """Contains Report Code and a Fight ID."""

    code: str
    """ID of the Report. eg.: tZVAxLYg7kTz1PBm"""

    startTime: datetime.datetime
    """Report Start Time."""

    fightID: int
    """ID of the Fight."""


class CharacterRanking(BaseModel):
    """Represents a Character/Player on the Rankings for a given Boss/Difficulty/Metric.
    Ref: https://www.warcraftlogs.com/v2-api-docs/warcraft/encounter.doc.html

    """

    name: str
    """The Charaters Name (no Realm)."""

    class_: str = Field(alias="class")
    """Name of the Class in CamelCase. (eg.: "DeathKnight")."""

    spec: str
    """Name of the Spec in CamelCase. (eg.: "BeastMastery")."""

    amount: float
    """total DPS/HPS."""

    duration: int
    """Fight duration in Milliseconds."""

    report: CharacterRankingReportFightData

    startTime: datetime.datetime
    """Fight Pull Time.."""

    hidden: bool = False


class CharacterRankings(BaseModel):
    page: int = 1
    hasMorePages: bool = False
    count: int = 0

    rankings: list[CharacterRanking] = []
