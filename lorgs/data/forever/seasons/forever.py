"""WoW Forever: the raids Warcraft Logs ranks so far (Phase 1: Onyxia).

The other Classic raids join once Warcraft Logs has zone and encounter ids for them.
"""

# IMPORT LOCAL LIBRARIES
from lorgs.data.expansions.classic import (
    ONYXIAS_LAIR,
)
from lorgs.data.forever.dungeons import DEADMINES, SHADOWFANG_KEEP, WAILING_CAVERNS
from lorgs.models.season import Season


FOREVER_SEASON = Season(
    name="WoW Forever",
    slug="forever",
    ilvl=0,
    raids=[
        ONYXIAS_LAIR,
    ],
    dungeons=[
        DEADMINES,
        WAILING_CAVERNS,
        SHADOWFANG_KEEP,
    ],
)
