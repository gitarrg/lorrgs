from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import datetime
import typing

# IMPORT THIRD PARTY LIBRARIES
from pydantic import BaseModel, field_validator, model_validator

# IMPORT LOCAL LIBRARIES
from .guild import Guild
from .report_events import ReportEvent
from .report_fight import ReportFight
from .report_master_data import ReportMasterData
from .report_summary import ReportSummary
from .user import User
from .zone import Zone


class Report(BaseModel):
    """A single report uploaded by a player to a guild or personal logs."""

    code: str = ""
    """The report code, a unique value used to identify the report."""

    title: str = ""
    """A title for the report."""

    startTime: datetime.datetime = datetime.datetime.fromtimestamp(0)
    """The start time of the report. Representing the timestamp of the first event contained in the report.."""

    endTime: datetime.datetime = datetime.datetime.fromtimestamp(0)
    """The end time of the report. Representing the timestamp of the last event contained in the report."""

    visibility: typing.Literal["public", "private", "unlisted"] = "public"
    """The visibility level of the report."""

    summary: ReportSummary | None = None
    """Summary Overview (queried via `table(..., dataType: Summary)`."""

    events: list[ReportEvent] = []
    """A set of report events, filterable via arguments like type, source, target, ability, etc."""

    masterData: ReportMasterData | None = None

    fights: list[ReportFight] = []

    zone: Zone = Zone(id=-1, name="unknown")

    owner: User = User(id=0, name="")
    """The user that uploaded the report."""

    guild: Guild | None = None
    """The guild that the report belongs to. If this is null, then the report was uploaded to the user's personal logs."""

    @field_validator("events", mode="before")
    @classmethod
    def unwrap_event_data(cls, v):
        """Events come in wraped in an ReportEventPaginator. Lets skip that step."""
        v = v or {}
        try:
            return v["data"]
        except KeyError:
            raise ValueError("Missing `data`.")


class ReportData(BaseModel):
    """The ReportData object enables the retrieval of single reports or filtered collections of reports."""

    report: Report

    @model_validator(mode="before")
    @classmethod
    def unwrap_data(cls, v):
        return (v and v.get("reportData")) or v
