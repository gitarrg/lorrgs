"""Stored timestamps load as timezone-aware UTC, including ones stored naive."""

import datetime
import json

import pytest

from lorgs.models.user import User
from lorgs.models.warcraftlogs_comp_ranking import CompRanking
from lorgs.models.warcraftlogs_ranking import SpecRanking
from lorgs.models.warcraftlogs_user_report import UserReport


NAIVE = "2026-10-18T12:00:00"
EXPECTED = datetime.datetime(2026, 10, 18, 12, 0, tzinfo=datetime.UTC)

STORED = [
    (User, {"discord_id": "123"}),
    (UserReport, {"report_id": "REPORT_ID"}),
    (
        SpecRanking,
        {"game_version": "retail", "spec_slug": "paladin-holy", "boss_slug": "nekzali", "difficulty": "mythic"},
    ),
    (CompRanking, {"game_version": "retail", "boss_slug": "nekzali"}),
]


@pytest.mark.parametrize(("model", "fields"), STORED)
def test_naive_stored_timestamp_loads_as_utc(model, fields) -> None:
    obj = model.model_validate_json(json.dumps({**fields, "updated": NAIVE}))

    assert obj.updated == EXPECTED
    assert obj.updated.tzinfo is not None


@pytest.mark.parametrize(("model", "fields"), STORED)
def test_aware_stored_timestamp_keeps_its_offset(model, fields) -> None:
    obj = model.model_validate_json(json.dumps({**fields, "updated": "2026-10-18T14:00:00+02:00"}))

    assert obj.updated == EXPECTED


@pytest.mark.parametrize(("model", "fields"), STORED)
def test_default_timestamp_is_aware(model, fields) -> None:
    obj = model(**fields)

    assert obj.updated.tzinfo is not None
    assert datetime.datetime.now(datetime.UTC) > obj.updated


def _stored_spec_ranking(updated: str, report_start: str, fight_start: str) -> SpecRanking:
    return SpecRanking.model_validate_json(
        json.dumps({
            "game_version": "retail",
            "spec_slug": "paladin-holy",
            "boss_slug": "nekzali",
            "difficulty": "mythic",
            "updated": updated,
            "reports": [
                {
                    "report_id": "REPORT_ID",
                    "start_time": report_start,
                    "fights": [{"fight_id": 1, "start_time": fight_start, "duration": 5000}],
                }
            ],
        })
    )


def test_naive_stored_report_and_fight_times_load_as_utc() -> None:
    ranking = _stored_spec_ranking(NAIVE, "2026-10-18T11:00:00", "2026-10-18T11:01:00")
    report = ranking.reports[0]
    fight = report.fights[0]

    assert report.start_time == EXPECTED - datetime.timedelta(hours=1)
    assert fight.start_time == EXPECTED - datetime.timedelta(minutes=59)
    assert fight.start_time_rel == 60_000
    assert fight.end_time_rel == 65_000


def test_mixed_naive_and_aware_stored_times_compare() -> None:
    ranking = _stored_spec_ranking(NAIVE, "2026-10-18T11:00:00Z", "2026-10-18T11:01:00")
    fight = ranking.reports[0].fights[0]

    assert fight.start_time_rel == 60_000
    assert fight.end_time > ranking.reports[0].start_time
    assert ranking.needs_refresh(now=EXPECTED + datetime.timedelta(hours=3)) is True
    assert ranking.needs_refresh(now=EXPECTED + datetime.timedelta(hours=1)) is False


def test_unloaded_report_start_time_has_a_timestamp() -> None:
    report = UserReport(report_id="REPORT_ID")

    assert report.start_time.tzinfo is not None
    assert isinstance(report.start_time.timestamp(), float)
