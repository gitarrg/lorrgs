"""War Within Season 2."""

# IMPORT LOCAL LIBRARIES
from lorgs.models.season import Season

# Dungeons
from lorgs.data.expansions.battle_for_azeroth import MECHAGON_WORKSHOP
from lorgs.data.expansions.battle_for_azeroth import THE_MOTHERLODE
from lorgs.data.expansions.shadowlands import THEATER_OF_PAIN
from lorgs.data.expansions.the_war_within import CINDERBREW_MEADERY
from lorgs.data.expansions.the_war_within import DARKFLAME_CLEFT
from lorgs.data.expansions.the_war_within import OPERATION_FLOODGATE
from lorgs.data.expansions.the_war_within import PRIORY_OF_THE_SACRED_FLAME
from lorgs.data.expansions.the_war_within import THE_ROOKERY

# Raids
from lorgs.data.expansions.the_war_within import LIBERATION_OF_UNDERMINE


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
