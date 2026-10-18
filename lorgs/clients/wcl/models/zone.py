# IMPORT THIRD PARTY LIBRARIES
from pydantic import BaseModel


class Zone(BaseModel):
    """A single zone from an expansion that represents a raid, dungeon, arena, etc.

    https://www.warcraftlogs.com/v2-api-docs/warcraft/zone.doc.html
    """

    id: int
    """The ID of the zone."""

    name: str = ""
    """The name of the zone."""
