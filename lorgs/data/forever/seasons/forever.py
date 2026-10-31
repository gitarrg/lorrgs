"""WoW Forever: all raids, since it has no seasons (so far)."""

# IMPORT LOCAL LIBRARIES
from lorgs.data.expansions.classic import (
    BLACKWING_LAIR,
    ONYXIAS_LAIR,
)
from lorgs.models.season import Season


FOREVER_SEASON = Season(
    name="WoW Forever",
    slug="forever",
    ilvl=0,
    raids=[
        ONYXIAS_LAIR,
        BLACKWING_LAIR,
    ],
    dungeons=[],
)
