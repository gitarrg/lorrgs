"""Mists of Pandaria Classic: all raid tiers. It has no seasons, so this one Season covers the whole expansion."""

# IMPORT LOCAL LIBRARIES
from lorgs.data.expansions.mists_of_pandaria import (
    HEART_OF_FEAR,
    MOGUSHAN_VAULTS,
    SIEGE_OF_ORGRIMMAR,
    TERRACE_OF_ENDLESS_SPRING,
    THRONE_OF_THUNDER,
)
from lorgs.models.season import Season


MISTS_SEASON = Season(
    name="WoW Classic: Mists of Pandaria",
    slug="mists",
    ilvl=0,
    raids=[
        MOGUSHAN_VAULTS,
        HEART_OF_FEAR,
        TERRACE_OF_ENDLESS_SPRING,
        THRONE_OF_THUNDER,
        SIEGE_OF_ORGRIMMAR,
    ],
    dungeons=[],
)
