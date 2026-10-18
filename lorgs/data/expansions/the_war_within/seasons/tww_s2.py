"""War Within Season 2."""

# IMPORT LOCAL LIBRARIES
# Dungeons
from lorgs.data.expansions.battle_for_azeroth import MECHAGON_WORKSHOP, THE_MOTHERLODE
from lorgs.data.expansions.shadowlands import THEATER_OF_PAIN

# Raids
from lorgs.data.expansions.the_war_within import (
    CINDERBREW_MEADERY,
    DARKFLAME_CLEFT,
    LIBERATION_OF_UNDERMINE,
    OPERATION_FLOODGATE,
    PRIORY_OF_THE_SACRED_FLAME,
    THE_ROOKERY,
)
from lorgs.models.season import Season


TWW_SEASON2 = Season(
    name="TWW Season 2",
    slug="tww_2",
    ilvl=678,
    raids=[
        LIBERATION_OF_UNDERMINE,
    ],
    dungeons=[
        CINDERBREW_MEADERY,
        DARKFLAME_CLEFT,
        PRIORY_OF_THE_SACRED_FLAME,
        THE_ROOKERY,
        OPERATION_FLOODGATE,
        THEATER_OF_PAIN,
        MECHAGON_WORKSHOP,
        THE_MOTHERLODE,
    ],
)
