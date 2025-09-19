"""War Within Season 2."""

# IMPORT LOCAL LIBRARIES
from lorgs.models.season import Season

# Dungeons
from lorgs.data.expansions.shadowlands import HALLS_OF_ATONEMENT
from lorgs.data.expansions.shadowlands import TAZAVESH_GAMBIT
from lorgs.data.expansions.shadowlands import TAZAVESH_STREETS
from lorgs.data.expansions.the_war_within import ARA_KARA
from lorgs.data.expansions.the_war_within import DAWNBREAKER
from lorgs.data.expansions.the_war_within import ECODOME_ALDANI
from lorgs.data.expansions.the_war_within import OPERATION_FLOODGATE
from lorgs.data.expansions.the_war_within import PRIORY_OF_THE_SACRED_FLAME


# Raids
from lorgs.data.expansions.the_war_within import MANAFORGE_OMEGA


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
