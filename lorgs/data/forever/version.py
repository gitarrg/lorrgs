"""The Game Data and the Game Version of WoW Forever."""

# IMPORT LOCAL LIBRARIES
from lorgs.data.forever.classes import (
    DRUID,
    HUNTER,
    MAGE,
    PALADIN,
    PRIEST,
    ROGUE,
    SHAMAN,
    WARLOCK,
    WARRIOR,
)
from lorgs.data.forever.roles import ALL_ROLES
from lorgs.data.forever.seasons import FOREVER_SEASON
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.game_data import GameData
from lorgs.models.game_version import GameVersion


GAME_DATA = GameData(
    roles=ALL_ROLES,
    classes=[
        DRUID,
        HUNTER,
        MAGE,
        PALADIN,
        PRIEST,
        ROGUE,
        SHAMAN,
        WARLOCK,
        WARRIOR,
    ],
    season=FOREVER_SEASON,
    difficulties=(RaidDifficulty.NORMAL,),
)

GAME_VERSION = GameVersion(
    name="forever",
    title="WoW Forever",
    wcl_game_version=99,  # placeholder until #86
    data=GAME_DATA,
    collapse_raids=True,
    has_comp_modes=False,
)
