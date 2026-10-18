from __future__ import annotations

from pydantic import BaseModel

from .report_actor import ReportActor


class ReportMasterData(BaseModel):
    """The ReporMastertData object contains information about the log version of a report,
    as well as the actors and abilities used in the report.

    """  # ruff: ignore[missing-blank-line-after-summary]

    actors: list[ReportActor]
    """A list of every actor (player, NPC, pet) that occurs in the report."""
