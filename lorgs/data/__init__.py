"""All the Constant Data for Lorrgs.

Each Game Version has its own package here, holding its roles, classes, specs, spells and raids,
and ending in a `GameVersion` that owns its `GameData`. Importing this package loads every Game Version.

This could be stored in a Database instead..
but at the end of the day, this was the most straight forward way and the easiest to manage.

"""

# IMPORT LOCAL LIBRARIES
from lorgs.data import forever, mists, retail
from lorgs.models.game_version import GameVersion


RETAIL = retail.GAME_VERSION
MISTS = mists.GAME_VERSION
FOREVER = forever.GAME_VERSION

GAME_VERSIONS: dict[str, GameVersion] = {version.name: version for version in (RETAIL, MISTS, FOREVER)}
"""All Game Versions by name. The order is the order of the frontend's Game Version menu."""


def get_game_version(name: str) -> GameVersion:
    """The Game Version with the given name. Raises a `KeyError` for unknown names."""
    return GAME_VERSIONS[name]


def get_game_version_by_wcl_id(wcl_game_version: int) -> GameVersion | None:
    """The Game Version whose logs carry the given Warcraft Logs `gameVersion` id."""
    return next((v for v in GAME_VERSIONS.values() if v.wcl_game_version == wcl_game_version), None)
