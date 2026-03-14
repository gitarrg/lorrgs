"""Midnight Season 1."""

# IMPORT LOCAL LIBRARIES
from lorgs.models.season import Season

# Dungeons


# Raids
from lorgs.data.expansions.midnight.raids import VOIDSPIRE
from lorgs.data.expansions.midnight.raids import DREAMRIFT
from lorgs.data.expansions.midnight.raids import MARCH_ON_QUALDANAS


MIDNIGHT_SEASON1 = Season(
    name="TWW Season 1",
    slug="tww_s1",
    ilvl=639,
    raids=[
        VOIDSPIRE,
        DREAMRIFT,
        MARCH_ON_QUALDANAS,
    ],
    dungeons=[],
)
