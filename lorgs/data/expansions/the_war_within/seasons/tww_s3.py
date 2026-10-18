"""War Within Season 2."""

# IMPORT LOCAL LIBRARIES
# Dungeons
from lorgs.data.expansions.shadowlands import HALLS_OF_ATONEMENT, TAZAVESH_GAMBIT, TAZAVESH_STREETS

# Raids
from lorgs.data.expansions.the_war_within import (
    ARA_KARA,
    DAWNBREAKER,
    ECODOME_ALDANI,
    MANAFORGE_OMEGA,
    OPERATION_FLOODGATE,
    PRIORY_OF_THE_SACRED_FLAME,
)
from lorgs.models.season import Season


TWW_SEASON3 = Season(
    name="TWW Season 3",
    slug="tww_3",
    ilvl=723,
    raids=[
        MANAFORGE_OMEGA,
    ],
    dungeons=[
        ARA_KARA,
        DAWNBREAKER,
        ECODOME_ALDANI,
        HALLS_OF_ATONEMENT,
        OPERATION_FLOODGATE,
        PRIORY_OF_THE_SACRED_FLAME,
        TAZAVESH_GAMBIT,
        TAZAVESH_STREETS,
    ],
)
