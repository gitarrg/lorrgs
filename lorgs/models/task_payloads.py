"""Typed payloads for SQS task messages.

These models define the contract between message producers (API routes, scripts)
and consumers (SQS task handlers). Every SQS message body should be serialized
from one of these models.
"""

from __future__ import annotations

from pydantic import BaseModel, field_validator

from lorgs.data import GAME_VERSIONS
from lorgs.models.game_version import GameVersion
from lorgs.models.raid_zone import AUTO_DIFFICULTY


class BaseTaskPayload(BaseModel):
    """Base for all SQS task payloads."""

    task: str

    game_version: str
    """Name of the Game Version the task runs for."""

    @field_validator("game_version")
    @classmethod
    def _known_game_version(cls, value: str) -> str:
        if value not in GAME_VERSIONS:
            raise ValueError(f"Unknown Game Version: {value!r}")
        return value

    def get_game_version(self) -> GameVersion:
        return GAME_VERSIONS[self.game_version]


class SpecRankingPayload(BaseTaskPayload):
    """Payload to load rankings for a single spec/boss combination."""

    task: str = "load_spec_rankings"
    boss_slug: str
    spec_slug: str
    difficulty: str = AUTO_DIFFICULTY
    metric: str = "dps"
    limit: int = 50
    clear: bool = False


class CompRankingPayload(BaseTaskPayload):
    """Payload to load comp (group composition) rankings for a boss."""

    task: str = "load_comp_rankings"
    boss_slug: str
    page: int = 1
    clear: bool = False


class UserReportPayload(BaseTaskPayload):
    """Payload to load specific fights/players from a user-submitted report."""

    task: str = "load_user_report"
    report_id: str
    user_id: int = 0
    fight_ids: list[int]
    player_ids: list[int]
