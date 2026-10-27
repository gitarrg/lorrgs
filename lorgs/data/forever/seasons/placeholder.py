"""Placeholder Season, so the Forever deployment has a current Season while it has no Raids."""

# IMPORT LOCAL LIBRARIES
from lorgs.models.season import Season


FOREVER_PLACEHOLDER_SEASON = Season(
    name="WoW Forever",
    slug="forever",
    ilvl=0,
    raids=[],
    dungeons=[],
)
