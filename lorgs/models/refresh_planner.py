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

POINTS_PER_REFRESH = 80
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

OFF_METRIC_REFRESH_INTERVAL = datetime.timedelta(hours=23)
"""Minimum time between Refreshes of an off-metric ranking (a metric other than its spec's default, eg.: dps for healers).

23h rather than 24h: the planner runs at the start of the hour but S3 `LastModified` is a few minutes later,
so a strict 24h would slip the refresh an hour later every day.
"""

NEVER = datetime.datetime.min.replace(tzinfo=datetime.UTC)
"""Last refreshed time of a ranking without a stored object: before every stored ranking."""


@dataclasses.dataclass(frozen=True)
class Candidate:
    """One Spec Ranking considered for a Refresh."""

    key: str
    """The ranking's S3 key (unique across Game Versions)."""

    last_refreshed: datetime.datetime | None
    """S3 `LastModified`. None when the ranking has no S3 object yet."""

    dirty_since: datetime.datetime | None = None
    """When the ranking was flagged Dirty (the marker's `LastModified`). None when it is not Dirty."""

    refresh_interval: datetime.timedelta = datetime.timedelta(0)
    """Minimum time between Refreshes. Dirty and never stored rankings ignore it."""

    def is_due(self, now: datetime.datetime) -> bool:
        """Whether the ranking may be refreshed now."""
        if self.dirty_since or self.last_refreshed is None:
            return True
        return now - self.last_refreshed >= self.refresh_interval


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


def _sort_key(candidate: Candidate) -> tuple[int, datetime.datetime]:
    if candidate.dirty_since:
        return (0, candidate.dirty_since)
    return (1, candidate.last_refreshed or NEVER)


def sort_stalest_first(candidates: Iterable[Candidate]) -> list[Candidate]:
    """Dirty rankings first (flagged longest ago first), then those without a stored object, then oldest first."""
    return sorted(candidates, key=_sort_key)


def plan(candidates: Iterable[Candidate], budget: int, now: datetime.datetime | None = None) -> list[Candidate]:
    """The stalest `budget` candidates that are due."""
    now = now or datetime.datetime.now(datetime.UTC)
    candidates = [c for c in candidates if c.is_due(now)]  # filter out the ones that are not due yet
    return sort_stalest_first(candidates)[:budget]


def make_candidates(
    keys: Iterable[str],  # a Mapping with the keys is fine too
    last_modified: Mapping[str, datetime.datetime],
    dirty: Mapping[str, datetime.datetime] | None = None,
) -> list[Candidate]:
    """Pair every ranking key with its S3 `LastModified` (if stored) and when it was flagged Dirty (if it is)."""
    dirty = dirty or {}
    return [Candidate(key, last_modified.get(key), dirty.get(key)) for key in keys]
