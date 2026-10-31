# IMPORT THIRD PARTY LIBRARIES
from pydantic import BaseModel

# IMPORT LOCAL LIBRARIES
from .report_data import Report, ReportData
from .world_data import WorldData


class MissingQueryResultError(ValueError):
    """The query result lacks the root field the loader asked for."""


class Query(BaseModel):
    """Root Query Object: the shape `WarcraftlogsClient.query` returns.

    Every loader parses its result through this model.

    ref: https://www.warcraftlogs.com/v2-api-docs/warcraft/query.doc.html
    """

    reportData: ReportData | None = None
    """Obtain the report data object that allows the retrieval of individual reports
    or filtered collections of reports by guild or by user."""

    worldData: WorldData | None = None
    """The world data object contains collections of data such as
    expansions, zones, encounters, regions, subregions, etc."""

    @property
    def report(self) -> Report:
        """The report of a query on `reportData`."""
        if self.reportData is None:
            raise MissingQueryResultError("Query result has no `reportData`.")
        return self.reportData.report

    @property
    def world_data(self) -> WorldData:
        """The world data of a query on `worldData`."""
        if self.worldData is None:
            raise MissingQueryResultError("Query result has no `worldData`.")
        return self.worldData
