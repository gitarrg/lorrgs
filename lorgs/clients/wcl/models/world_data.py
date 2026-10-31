from pydantic import BaseModel

from .encounter import Encounter


class WorldData(BaseModel):
    """The world data object contains collections of data such as
    expansions, zones, encounters, regions, subregions, etc.
    """  # ruff: ignore[missing-blank-line-after-summary]

    encounter: Encounter = Encounter()
    """Obtain a specific encounter by id."""
