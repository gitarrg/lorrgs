"""The Game Version (Retail, WoW Forever, ...) this deployment serves.

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


ENV_VAR = "LORRGS_GAME_VERSION"
DEFAULT_NAME = "retail"


@dataclasses.dataclass(frozen=True)
class GameVersion:
    """Static configuration of one Game Version."""

    name: str

    s3_prefix: str
    """Prefix for all S3 keys. Empty for Retail, so its existing keys stay as they are."""

    difficulties: tuple[RaidDifficulty, ...]
    """Difficulties we rank. The last entry is the default."""

    wcl_game_versions: frozenset[int]
    """WCL `masterData.gameVersion` ids of logs that belong to this Game Version."""

    data_package: str
    """Dotted path of the package holding this Game Version's game data (not imported here)."""

    @property
    def default_difficulty(self) -> RaidDifficulty:
        return self.difficulties[-1]


RETAIL = GameVersion(
    name="retail",
    s3_prefix="",
    difficulties=(RaidDifficulty.HEROIC, RaidDifficulty.MYTHIC),
    wcl_game_versions=frozenset({1}),
    data_package="lorgs.data.retail",
)

FOREVER = GameVersion(
    name="forever",
    s3_prefix="forever/",
    difficulties=(RaidDifficulty.NORMAL,),
    wcl_game_versions=frozenset(),  # placeholder until #86
    data_package="lorgs.data.forever",
)

GAME_VERSIONS: dict[str, GameVersion] = {gv.name: gv for gv in (RETAIL, FOREVER)}


def resolve(name: str | None) -> GameVersion:
    """Look up a Game Version by name (case-insensitive). Empty/None means the default.

    Raises:
        ValueError: if `name` is not a known Game Version.

    """
    key = (name or "").strip().lower() or DEFAULT_NAME
    try:
        return GAME_VERSIONS[key]
    except KeyError:
        valid = ", ".join(sorted(GAME_VERSIONS))
        msg = f"Invalid {ENV_VAR}={name!r}. Expected one of: {valid}"
        raise ValueError(msg) from None


ACTIVE: GameVersion = resolve(os.getenv(ENV_VAR))
