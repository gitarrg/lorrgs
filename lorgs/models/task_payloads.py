"""Typed payloads for SQS task messages.

These models define the contract between message producers (API routes, scripts)
and consumers (SQS task handlers). Every SQS message body should be serialized
from one of these models.
"""

from __future__ import annotations

from pydantic import BaseModel


class BaseTaskPayload(BaseModel):
    """Base for all SQS task payloads."""

    task: str


class SpecRankingPayload(BaseTaskPayload):
    """Payload to load rankings for a single spec/boss combination."""

    task: str = "load_spec_rankings"
    boss_slug: str
    spec_slug: str
    difficulty: str = "mythic"
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
