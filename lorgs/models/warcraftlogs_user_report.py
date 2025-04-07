"""Classes/Functions to manage Reports injected through user interaction."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing
import datetime

# IMPORT LOCAL LIBRARIES
from lorgs.models import base
from lorgs.models.warcraftlogs_report import Report


TTL_DURATION = datetime.timedelta(days=365)


class UserReport(Report, base.DynamoDBModel):
    """A single report loaded via the custom reports module.

    Todo:
        * Test performance when splitting each report into its own row,
          saved with the same partion, but different secondary key

    """

    # datetime: timetamp of last update
    updated: datetime.datetime = datetime.datetime.min
    ttl: int = 0

    # Config
    pkey: typing.ClassVar[str] = "{report_id}"
    skey: typing.ClassVar[str] = "overview"

    ################################
    # Properties
    #
    @property
    def is_loaded(self) -> bool:
        return bool(self.fights)

    ################################
    # Methods
    #
    def save(self, *args: typing.Any, **kwargs: typing.Any) -> None:  # pylint: disable=arguments-differ
        """Update the timestamp and Save the Report."""
        self.updated = datetime.datetime.now(datetime.timezone.utc)

        ttl = self.updated + TTL_DURATION
        self.ttl = int(ttl.timestamp())

        return super().save(*args, **kwargs)
