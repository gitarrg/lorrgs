"""The Game Version (Retail, Classic, Forever, ...) this deployment serves.

Each deployment serves exactly one Game Version, picked by the `LORRGS_GAME_VERSION`
environment variable (default: `retail`). It is resolved once, at import time.

This module must stay free of game data: it only names the data package
(`GameVersion.data_package`) and never imports it.
"""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import dataclasses
import os

# IMPORT LOCAL LIBRARIES
from lorgs.models.difficulty import RaidDifficulty


@dataclasses.dataclass(frozen=True)
class GameVersion:
    """Static configuration of one Game Version."""

    name: str

    title: str
    """Display name for the frontend's Game Version menu."""

    s3_prefix: str
    """Prefix for all S3 keys. Empty for Retail, so its existing keys stay as they are."""

    difficulties: tuple[RaidDifficulty, ...]
    """Difficulties we rank. The last entry is the default."""

    wcl_game_version: int
    """WCL `masterData.gameVersion` id of the logs that belong to this Game Version."""

    data_package: str
    """Dotted path of the package holding this Game Version's game data (not imported here)."""

    collapse_raids: bool = False
    """Frontend: collapse all raids but the selected one in the navbar (for Game Versions with many raids)."""

    has_comp_modes: bool = True
    """Frontend: whether the Game Version has Comp Rankings (the home page hides them otherwise)."""

    @property
    def api_url(self) -> str:
        """Base URL of the deployment serving this Game Version, from `LORRGS_API_URL_<NAME>` (empty if unset).

        Lets the frontend, which talks to one deployment at a time, switch to another Game Version's API.
        """
        return os.getenv(f"LORRGS_API_URL_{self.name.upper()}", "").rstrip("/")

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


RETAIL = GameVersion(
    name="retail",
    title="Retail",
    s3_prefix="",
    difficulties=(RaidDifficulty.HEROIC, RaidDifficulty.MYTHIC),
    wcl_game_version=1,
    data_package="lorgs.data.retail",
)

FOREVER = GameVersion(
    name="forever",
    title="WoW Forever",
    s3_prefix="forever/",
    difficulties=(RaidDifficulty.NORMAL,),
    wcl_game_version=99,  # placeholder until #86
    data_package="lorgs.data.forever",
    collapse_raids=True,
    has_comp_modes=False,
)

CLASSIC_MOP = GameVersion(
    name="classic_mop",
    title="Classic: Mists of Pandaria",
    s3_prefix="classic_mop/",
    difficulties=(RaidDifficulty.NORMAL, RaidDifficulty.HEROIC),
    wcl_game_version=6,
    data_package="lorgs.data.classic_mop",
    collapse_raids=True,
    has_comp_modes=False,
)

GAME_VERSIONS: dict[str, GameVersion] = {}
GAME_VERSIONS[RETAIL.name] = RETAIL
GAME_VERSIONS[CLASSIC_MOP.name] = CLASSIC_MOP
GAME_VERSIONS[FOREVER.name] = FOREVER


current_game_version = os.getenv("LORRGS_GAME_VERSION") or RETAIL.name
ACTIVE = GAME_VERSIONS[current_game_version]
