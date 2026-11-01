"""The Refresh Planner: budget maths and stalest-first ordering (no AWS or Warcraft Logs calls)."""

import datetime

import pytest

from lorgs.models import refresh_planner
from lorgs.models.refresh_planner import Candidate


def _at(hour: int) -> datetime.datetime:
    return datetime.datetime(2026, 1, 1, hour, tzinfo=datetime.UTC)


@pytest.mark.parametrize(
    ("limit", "spent", "max_refreshes", "expected"),
    [
        (18000, 0, None, 720),  # (18000 * 0.8) / 20
        (18000, 3600, None, 540),  # points already spent come off
        (18000, 14400, None, 0),  # only the reserve is left
        (18000, 17000, None, 0),  # never negative
        (18000, 0, 100, 100),  # cap below what points allow
        (18000, 0, 5000, 720),  # cap above: points limit
        (0, 0, None, 0),
    ],
)
def test_budget(limit: int, spent: int, max_refreshes: int | None, expected: int) -> None:
    assert refresh_planner.get_budget(limit, spent, cost=20, max_refreshes=max_refreshes) == expected


def test_budget_uses_the_given_reserve_and_cost() -> None:
    assert refresh_planner.get_budget(1000, 0, reserve=0.5, cost=10, max_refreshes=None) == 50


def test_oldest_first() -> None:
    candidates = [Candidate("b", _at(5)), Candidate("a", _at(1)), Candidate("c", _at(3))]

    assert [c.key for c in refresh_planner.sort_stalest_first(candidates)] == ["a", "c", "b"]


def test_rankings_missing_from_s3_come_first() -> None:
    candidates = [
        Candidate("old", _at(0)),
        Candidate("new", None),
        Candidate("older", datetime.datetime.min.replace(tzinfo=datetime.UTC)),
    ]

    assert [c.key for c in refresh_planner.sort_stalest_first(candidates)][0] in {"new", "older"}
    assert refresh_planner.sort_stalest_first(candidates)[-1].key == "old"


def test_plan_takes_the_stalest_within_the_budget() -> None:
    candidates = [Candidate("b", _at(5)), Candidate("x", None), Candidate("a", _at(1))]

    assert [c.key for c in refresh_planner.plan(candidates, 2)] == ["x", "a"]
    assert refresh_planner.plan(candidates, 0) == []


def test_make_candidates_pairs_keys_with_last_modified() -> None:
    result = refresh_planner.make_candidates(["a", "b"], {"a": _at(2), "other": _at(3)})

    assert result == [Candidate("a", _at(2)), Candidate("b", None)]


def test_dirty_rankings_come_first_oldest_flag_first() -> None:
    candidates = [
        Candidate("stale", _at(1)),
        Candidate("missing", None),
        Candidate("dirty-new", _at(9), dirty_since=_at(8)),
        Candidate("dirty-old", _at(9), dirty_since=_at(2)),
    ]

    assert [c.key for c in refresh_planner.sort_stalest_first(candidates)] == [
        "dirty-old",
        "dirty-new",
        "missing",
        "stale",
    ]


def test_dirty_rankings_count_against_the_budget() -> None:
    candidates = [Candidate(f"d{i}", _at(1), dirty_since=_at(i)) for i in range(5)] + [Candidate("stale", None)]

    assert [c.key for c in refresh_planner.plan(candidates, 3)] == ["d0", "d1", "d2"]


def test_make_candidates_takes_dirty_since_from_the_markers() -> None:
    result = refresh_planner.make_candidates(["a", "b"], {"a": _at(2), "b": _at(3)}, {"b": _at(4)})

    assert result == [Candidate("a", _at(2)), Candidate("b", _at(3), _at(4))]
