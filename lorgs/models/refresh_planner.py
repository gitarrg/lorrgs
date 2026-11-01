"""Plan the Spec Ranking Refreshes of the next hour: the stalest rankings that fit the Refresh Budget.

Pure maths and ordering. Reading S3 and Warcraft Logs is up to the caller.
"""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import dataclasses
import datetime
import typing


if typing.TYPE_CHECKING:
    from collections.abc import Iterable, Mapping


POINTS_RESERVE = 0.2
"""Share of the hourly Warcraft Logs points kept for User Reports and manual refreshes."""

POINTS_PER_REFRESH = 40
"""Estimated cost of one Refresh (see `scripts/measure_wcl_points.py`).

Each query, the minimum of the readings:

| Query             | Points |
| ----------------- |--------|
| characterRankings | 2      |
| boss              | 2      |
| player            | 4      |

One Refresh of 10 reports:
| Query             | Points |
| ----------------- |--------|
| characterRankings | 2      |
| boss              | 2      |
| 10 reports        | 40     |
| total             | 44     |
"""

MAX_REFRESHES_PER_HOUR: int | None = None
"""Cap on Refreshes per hour. Stands in for Warcraft Logs' Database points once we opt in. None: no cap."""

NEVER = datetime.datetime.min.replace(tzinfo=datetime.UTC)
"""Last refreshed time of a ranking without a stored object: before every stored ranking."""


@dataclasses.dataclass(frozen=True)
class Candidate:
    """One Spec Ranking considered for a Refresh."""

    key: str
    """The ranking's S3 key (unique across Game Versions)."""

    last_refreshed: datetime.datetime | None
    """S3 `LastModified`. None when the ranking has no S3 object yet."""


def get_budget(
    limit_per_hour: int,
    points_spent: int,
    *,
    reserve: float = POINTS_RESERVE,
    cost: int = POINTS_PER_REFRESH,
    max_refreshes: int | None = MAX_REFRESHES_PER_HOUR,
) -> int:
    """How many Refreshes fit this hour: points left after the reserve, divided by the cost, capped."""
    points = limit_per_hour * (1 - reserve) - points_spent
    refreshes = max(0, int(points // cost))
    if max_refreshes is not None:
        refreshes = min(refreshes, max_refreshes)
    return refreshes


def sort_stalest_first(candidates: Iterable[Candidate]) -> list[Candidate]:
    """Rankings without a stored object first, then the oldest Refresh first. Ties keep their order."""
    return sorted(candidates, key=lambda c: c.last_refreshed or NEVER)


def plan(candidates: Iterable[Candidate], budget: int) -> list[Candidate]:
    """The stalest `budget` candidates."""
    return sort_stalest_first(candidates)[:budget]


def make_candidates(keys: Iterable[str], last_modified: Mapping[str, datetime.datetime]) -> list[Candidate]:
    """Pair every ranking key with its S3 `LastModified`, if stored."""
    return [Candidate(key, last_modified.get(key)) for key in keys]
