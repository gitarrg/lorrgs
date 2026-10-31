"""Static configuration of one Game Version (Retail, Classic, Forever, ...)."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import dataclasses
import typing


if typing.TYPE_CHECKING:
    from lorgs.models.difficulty import RaidDifficulty
    from lorgs.models.game_data import GameData


@dataclasses.dataclass(frozen=True)
class GameVersion:
    """One Game Version and its Game Data.

    Defined next to the Game Data in the Game Version's package under `lorgs/data/`.
    """

    name: str

    title: str
    """Display name for the frontend's Game Version menu."""

    wcl_game_version: int
    """WCL `masterData.gameVersion` id of the logs that belong to this Game Version."""

    data: GameData
    """The Version's Game Data"""

    collapse_raids: bool = False
    """Frontend: collapse all raids but the selected one in the navbar (for Game Versions with many raids)."""

    has_comp_modes: bool = True
    """Frontend: whether the Game Version has Comp Rankings (the home page hides them otherwise)."""

    has_talents: bool = False
    """Whether Spec Rankings store each player's Talents (Retail only)."""

    @property
    def difficulties(self) -> tuple[RaidDifficulty, ...]:
        """Difficulties we rank. The last entry is the default."""
        return self.data.difficulties

    @property
    def default_difficulty(self) -> RaidDifficulty:
        return self.data.default_difficulty

    @property
    def difficulty_names(self) -> tuple[str, ...]:
        return self.data.difficulty_names

    @property
    def default_difficulty_name(self) -> str:
        return self.data.default_difficulty_name

    @property
    def s3_prefix(self) -> str:
        """Prefix for all S3 keys of this Game Version."""
        return f"{self.name}/"
