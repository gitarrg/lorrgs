"""Static configuration of one Game Version (Retail, Classic, Forever, ...)."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import dataclasses
import functools
import importlib
import os
import typing


if typing.TYPE_CHECKING:
    from lorgs.models.game_data import GameData
    from lorgs.models.difficulty import RaidDifficulty


@dataclasses.dataclass(frozen=True)
class GameVersion:
    """Static configuration of one Game Version."""

    name: str

    title: str
    """Display name for the frontend's Game Version menu."""

    difficulties: tuple[RaidDifficulty, ...]
    """Difficulties we rank. The last entry is the default."""

    wcl_game_version: int
    """WCL `masterData.gameVersion` id of the logs that belong to this Game Version."""

    collapse_raids: bool = False
    """Frontend: collapse all raids but the selected one in the navbar (for Game Versions with many raids)."""

    has_comp_modes: bool = True
    """Frontend: whether the Game Version has Comp Rankings (the home page hides them otherwise)."""

    ####################################################################################################################
    # Game Data
    ####################################################################################################################

    @property
    def data_package(self) -> str:
        """Dotted path of the package holding this Game Version's game data."""
        return f"lorgs.data.{self.name}"

    @functools.cached_property
    def data(self) -> GameData:
        """This Game Version's Game Data. Imported on first access, so this module stays free of game data."""
        return importlib.import_module(self.data_package).GAME_DATA

    @property
    def default_difficulty(self) -> RaidDifficulty:
        return self.difficulties[-1]

    @property
    def difficulty_names(self) -> tuple[str, ...]:
        """The difficulties as the lowercase names used in API routes, task payloads and S3 keys."""
        return tuple(difficulty.name.lower() for difficulty in self.difficulties)

    @property
    def default_difficulty_name(self) -> str:
        return self.default_difficulty.name.lower()

    ####################################################################################################################
    # AWS Resources
    ####################################################################################################################

    @property
    def deploy_prefix(self) -> str:
        """Prefix of this Game Version's AWS resource names (Lambdas, queues, schedules)."""
        return f"{self.name}-"

    @property
    def s3_prefix(self) -> str:
        """Prefix for all S3 keys."""
        return f"{self.name}/"

    @property
    def api_url(self) -> str:
        """Base URL of the deployment serving this Game Version."""
        return f"{self.name}-api.lorrgs.io"
