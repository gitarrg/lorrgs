"""The Game Data and the Game Version of Retail."""

# IMPORT LOCAL LIBRARIES
from lorgs.data.retail.classes import (
    DEATHKNIGHT,
    DEMONHUNTER,
    DRUID,
    EVOKER,
    HUNTER,
    MAGE,
    MONK,
    OTHER,
    PALADIN,
    PRIEST,
    ROGUE,
    SHAMAN,
    WARLOCK,
    WARRIOR,
)
from lorgs.data.retail.classes.other import ITEM_ROLE, UTIL_ROLE
from lorgs.data.retail.racials import RACIALS
from lorgs.data.retail.roles import ALL_ROLES, MIXED
from lorgs.data.retail.season import CURRENT_SEASON
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.game_data import GameData
from lorgs.models.game_version import GameVersion


GAME_DATA = GameData(
    roles=[
        *ALL_ROLES,
        MIXED,
        ITEM_ROLE,
        UTIL_ROLE,
    ],
    classes=[
        DEATHKNIGHT,
        DEMONHUNTER,
        DRUID,
        EVOKER,
        HUNTER,
        MAGE,
        MONK,
        OTHER,
        PALADIN,
        PRIEST,
        ROGUE,
        SHAMAN,
        WARLOCK,
        WARRIOR,
        RACIALS,
    ],
    season=CURRENT_SEASON,
    difficulties=(
        RaidDifficulty.HEROIC,
        RaidDifficulty.MYTHIC,
    ),
)

GAME_VERSION = GameVersion(
    name="retail",
    title="Retail",
    wcl_game_version=1,
    data=GAME_DATA,
)
