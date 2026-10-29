"""FastAPI dependencies shared by the routes."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import enum
import typing

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs.data import GAME_VERSIONS
from lorgs.models.game_version import GameVersion


GameVersionName = enum.StrEnum("GameVersionName", {name: name for name in GAME_VERSIONS})
"""The names of all Game Versions. As the type of the path parameter it lists them in the OpenAPI docs."""


def get_game_version(game_version: GameVersionName) -> GameVersion:
    """Resolve the `{game_version}` path parameter. Unknown names are rejected with a 422."""
    return GAME_VERSIONS[game_version.value]


GameVersionDep = typing.Annotated[GameVersion, fastapi.Depends(get_game_version)]
