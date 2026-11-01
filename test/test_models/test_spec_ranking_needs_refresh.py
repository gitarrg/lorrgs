"""Refresh policy for a Spec Ranking."""

import datetime

from lorgs.models.warcraftlogs_ranking import SpecRanking
from lorgs.models.warcraftlogs_report import Report


NOW = datetime.datetime(2026, 10, 18, 12, 0, tzinfo=datetime.UTC)


def _ranking(
    *,
    report_count: int = 2,
    updated: datetime.datetime | None = None,
    dirty: bool = False,
) -> SpecRanking:
    return SpecRanking(
        game_version="retail",
        difficulty="mythic",
        spec_slug="paladin-holy",
        boss_slug="nekzali",
        reports=[Report(report_id=f"report-{index}") for index in range(report_count)],
        updated=NOW - datetime.timedelta(minutes=30) if updated is None else updated,
        dirty=dirty,
    )


def test_dirty_ranking_refreshes_even_when_recent() -> None:
    ranking = _ranking(dirty=True)

    assert ranking.needs_refresh(now=NOW) is True


def test_clean_stale_ranking_refreshes() -> None:
    ranking = _ranking(updated=NOW - datetime.timedelta(hours=2, seconds=1))

    assert ranking.needs_refresh(now=NOW) is True


def test_clean_recent_ranking_skips() -> None:
    ranking = _ranking(updated=NOW - datetime.timedelta(hours=2))

    assert ranking.needs_refresh(now=NOW) is False


def test_few_reports_do_not_force_a_refresh_when_recent() -> None:
    ranking = _ranking(report_count=0)

    assert ranking.needs_refresh(now=NOW) is False


def test_never_refreshed_ranking_refreshes() -> None:
    ranking = SpecRanking(game_version="retail", difficulty="mythic", spec_slug="paladin-holy", boss_slug="nekzali")

    assert ranking.needs_refresh(now=NOW) is True


def test_naive_recent_timestamp_is_treated_as_utc() -> None:
    updated = (NOW - datetime.timedelta(minutes=30)).replace(tzinfo=None)
    ranking = _ranking(updated=updated)

    assert ranking.needs_refresh(now=NOW) is False


def test_naive_stale_timestamp_is_treated_as_utc() -> None:
    updated = (NOW - datetime.timedelta(hours=3)).replace(tzinfo=None)
    ranking = _ranking(updated=updated)

    assert ranking.needs_refresh(now=NOW) is True
