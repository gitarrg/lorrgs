"""The Game Data and the Game Version of WoW Classic: Mists of Pandaria."""

# IMPORT LOCAL LIBRARIES
from lorgs.data.mists.classes import (
    DEATHKNIGHT,
    DRUID,
    HUNTER,
    MAGE,
    MONK,
    PALADIN,
    PRIEST,
    ROGUE,
    SHAMAN,
    WARLOCK,
    WARRIOR,
)
from lorgs.data.mists.roles import ALL_ROLES
from lorgs.data.mists.seasons import MISTS_PHASE5
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.game_data import GameData
from lorgs.models.game_version import GameVersion


GAME_DATA = GameData(
    roles=ALL_ROLES,
    classes=[
        DEATHKNIGHT,
        DRUID,
        HUNTER,
        MAGE,
        MONK,
        PALADIN,
        PRIEST,
        ROGUE,
        SHAMAN,
        WARLOCK,
        WARRIOR,
    ],
    season=MISTS_PHASE5,
    difficulties=(RaidDifficulty.HEROIC,),
)

GAME_VERSION = GameVersion(
    name="mists",
    title="Classic: Mists of Pandaria",
    wcl_game_version=6,
    data=GAME_DATA,
    collapse_raids=True,
    has_comp_modes=False,
)
