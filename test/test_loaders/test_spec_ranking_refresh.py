"""Spec Ranking Refresh skips reports Warcraft Logs will not show."""

import asyncio
import datetime
import logging

import pytest

import lorgs.data  # noqa: F401  # registers specs and bosses
from lorgs.clients.wcl.client import PrivateReportError, UnknownReportError
from lorgs.loaders.spec_ranking import SpecRankingLoader
from lorgs.models.warcraftlogs_boss import Boss
from lorgs.models.warcraftlogs_cast import Cast
from lorgs.models.warcraftlogs_fight import Fight, Phase
from lorgs.models.warcraftlogs_player import Player
from lorgs.models.warcraftlogs_ranking import SpecRanking
from lorgs.models.warcraftlogs_report import Report


GOOD_REPORT = "goodreport000001"
PRIVATE_REPORT = "privatereport001"


def _ranking_row(*, name: str, amount: float, code: str, fight_id: int) -> dict[str, object]:
    return {
        "name": name,
        "class": "Paladin",
        "spec": "Holy",
        "amount": amount,
        "duration": 120000,
        "startTime": 1634544096374,
        "report": {
            "code": code,
            "fightID": fight_id,
            "startTime": 1634543354962,
        },
    }


RANKINGS = {
    "worldData": {
        "encounter": {
            "characterRankings": {
                "rankings": [
                    _ranking_row(name="Skipped", amount=200, code=PRIVATE_REPORT, fight_id=5),
                    _ranking_row(name="Kept", amount=100, code=GOOD_REPORT, fight_id=8),
                ],
            },
        },
    },
}


class FakeWarcraftlogsClient:
    """Warcraft Logs stand-in: one report is refused, everything else loads."""

    def __init__(self, refused: type[Exception]) -> None:
        self.refused = refused

    async def query(self, query: str) -> dict[str, object]:
        if PRIVATE_REPORT in query:
            raise self.refused("You do not have permission to view this report.")
        if "characterRankings" in query:
            return RANKINGS
        return {"reportData": {"report": {"events": {"data": []}, "fights": []}}}


def _refresh(caplog: pytest.LogCaptureFixture, refused: type[Exception]) -> SpecRanking:
    ranking = SpecRanking(
        spec_slug="paladin-holy",
        boss_slug="nekzali-the-soulcoiler",
        metric="hps",
    )
    with caplog.at_level(logging.WARNING, logger="Lorgs"):
        asyncio.run(SpecRankingLoader(ranking).load(client=FakeWarcraftlogsClient(refused), limit=10))
    return ranking


def test_refresh_drops_a_private_report_and_keeps_the_others(caplog: pytest.LogCaptureFixture) -> None:
    ranking = _refresh(caplog, PrivateReportError)

    assert [report.report_id for report in ranking.reports] == [GOOD_REPORT]
    assert PRIVATE_REPORT in caplog.text


def test_refresh_drops_a_deleted_report_and_keeps_the_others(caplog: pytest.LogCaptureFixture) -> None:
    ranking = _refresh(caplog, UnknownReportError)

    assert [report.report_id for report in ranking.reports] == [GOOD_REPORT]
    assert PRIVATE_REPORT in caplog.text


def test_refresh_drops_a_private_report_that_was_already_loaded(caplog: pytest.LogCaptureFixture) -> None:
    ranking = SpecRanking(
        spec_slug="paladin-holy",
        boss_slug="nekzali-the-soulcoiler",
        metric="hps",
        reports=[
            _stored_report(GOOD_REPORT, fight_id=8, name="Kept", amount=200),
            _stored_report(PRIVATE_REPORT, fight_id=5, name="Skipped", amount=100),
        ],
    )
    caplog.set_level(logging.WARNING, logger="Lorgs")

    asyncio.run(SpecRankingLoader(ranking).load(client=FakeWarcraftlogsClient(PrivateReportError), limit=10))

    assert [report.report_id for report in ranking.reports] == [GOOD_REPORT]
    assert PRIVATE_REPORT in caplog.text


def _stored_report(code: str, *, fight_id: int, name: str, amount: float) -> Report:
    return Report(
        report_id=code,
        start_time=datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC),
        fights=[
            Fight(
                fight_id=fight_id,
                start_time=datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC),
                duration=120000,
                players=[
                    Player(
                        name=name,
                        total=amount,
                        spec_slug="paladin-holy",
                        casts=[Cast(spell_id=1, timestamp=1)],
                    ),
                ],
                boss=Boss(boss_slug="nekzali-the-soulcoiler"),
                phases=[Phase(ts=1, phase_id=1)],
            ),
        ],
    )
