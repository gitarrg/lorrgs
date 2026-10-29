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
from lorgs.data.retail.items.midnight import MIDNIGHT_CONSUMABLES
from lorgs.data.retail.items.the_war_within import TWW_CONSUMABLES
from lorgs.data.retail.racials import RACIALS
from lorgs.data.retail.roles import ALL_ROLES, MIXED
from lorgs.data.retail.seasons import (
    MIDNIGHT_SEASON1,
    MIDNIGHT_SEASON2,
    TWW_SEASON1,
    TWW_SEASON2,
    TWW_SEASON3,
)
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
    seasons=[
        TWW_SEASON1,
        TWW_SEASON2,
        TWW_SEASON3,
        MIDNIGHT_SEASON1,
        MIDNIGHT_SEASON2,
    ],
    current_season=MIDNIGHT_SEASON2,
    difficulties=(
        RaidDifficulty.HEROIC,
        RaidDifficulty.MYTHIC,
    ),
    spells=[*MIDNIGHT_CONSUMABLES, *TWW_CONSUMABLES],
)

GAME_VERSION = GameVersion(
    name="retail",
    title="Retail",
    wcl_game_version=1,
    data=GAME_DATA,
)
