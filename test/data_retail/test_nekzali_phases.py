"""Boss-specific Phases are corrected once the Fight's Phases and boss Casts are both loaded."""

import asyncio
import datetime
import logging
from typing import override

import pytest

import lorgs.data  # noqa: F401  # registers specs and bosses
from lorgs.data import RETAIL
from lorgs.data.retail import GAME_DATA
from lorgs.data.expansions.midnight.raids.the_venomous_abyss.nekzali import (
    NEKZALI,
    RITUAL_OF_AWAKENING,
    SOUL_TRANSFER,
    UNCOILING_TRANSITION,
)
from lorgs.loaders.report_loader import ReportLoader
from lorgs.loaders.spec_ranking import SpecRankingLoader
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.warcraftlogs_boss import Boss
from lorgs.models.warcraftlogs_cast import Cast
from lorgs.models.warcraftlogs_fight import Fight, Phase
from lorgs.models.warcraftlogs_player import Player
from lorgs.models.warcraftlogs_ranking import SpecRanking
from lorgs.models.warcraftlogs_report import Report

from ..helpers import game_data_with, game_version_with


def test_other_bosses_phases_are_unchanged() -> None:
    """A boss without its own phase correction returns the Phases it was given."""
    boss = RaidBoss(id=90064, name="Plain Phase Boss")
    phases = [Phase(ts=10_000, phase_id=2), Phase(ts=20_000, phase_id=3)]
    casts = [Cast(spell_id=1, timestamp=5_000)]

    result = boss.process_phases(phases, casts)

    assert [(phase.phase_id, phase.timestamp) for phase in result] == [
        (2, 10_000),
        (3, 20_000),
    ]


def test_kill_with_intermissions_and_uncoiling_has_phases_at_the_right_times() -> None:
    """A kill keeps Phase 1, both intermissions, and Phase 2 at the Uncoiling transition."""
    phases = [
        Phase(ts=110_000, phase_id=2),
        Phase(ts=180_000, phase_id=UNCOILING_TRANSITION),
    ]
    casts = [
        Cast(spell_id=RITUAL_OF_AWAKENING, timestamp=90_000),
        Cast(spell_id=SOUL_TRANSFER, timestamp=120_000),
        Cast(spell_id=SOUL_TRANSFER, timestamp=150_000),
    ]

    result = NEKZALI.process_phases(phases, casts)

    assert [(phase.phase_id, phase.timestamp) for phase in result] == [
        (1, 0),
        (1.5, 90_000),
        (1.75, 135_000),
        (2, 180_000),
    ]


def test_phase_1_wipe_keeps_intermissions_and_does_not_add_phase_2() -> None:
    """A wipe that never reached Uncoiling still records intermissions found from Casts."""
    phases = [Phase(ts=50_000, phase_id=2)]
    casts = [
        Cast(spell_id=RITUAL_OF_AWAKENING, timestamp=80_000),
        Cast(spell_id=SOUL_TRANSFER, timestamp=100_000),
    ]

    result = NEKZALI.process_phases(phases, casts)

    assert [(phase.phase_id, phase.timestamp) for phase in result] == [
        (1, 0),
        (1.5, 80_000),
        (1.75, 85_000),
    ]


def test_nekzali_actor_load_does_not_rewrite_phases() -> None:
    """Loading the boss does not change Phases. Correction happens after both are loaded."""
    fight = Fight(
        fight_id=14,
        start_time=datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC),
        phases=[Phase(ts=180_000, phase_id=UNCOILING_TRANSITION)],
    )
    boss = Boss(boss_slug=NEKZALI.full_name_slug)
    boss.fight = fight
    boss.casts = [
        Cast(spell_id=RITUAL_OF_AWAKENING, timestamp=90_000),
        Cast(spell_id=SOUL_TRANSFER, timestamp=150_000),
    ]

    Boss.event_actor_load.send(boss, status="success")

    assert [(phase.phase_id, phase.timestamp) for phase in fight.phases] == [(UNCOILING_TRANSITION, 180_000)]


FIGHT_START_MS = 1_700_000_000_000
REPORT_CODE = "nekzreport000001"
FIGHT_ID = 14

KILL_PHASES = [
    (1, 0),
    (1.5, 90_000),
    (1.75, 135_000),
    (2, 180_000),
]


def _ranking_payload() -> dict[str, object]:
    return {
        "worldData": {
            "encounter": {
                "characterRankings": {
                    "rankings": [
                        {
                            "name": "Healer",
                            "class": "Paladin",
                            "spec": "Holy",
                            "amount": 100,
                            "duration": 300_000,
                            "startTime": FIGHT_START_MS,
                            "report": {
                                "code": REPORT_CODE,
                                "fightID": FIGHT_ID,
                                "startTime": FIGHT_START_MS,
                            },
                        },
                    ],
                },
            },
        },
    }


def _boss_events() -> dict[str, object]:
    return {
        "reportData": {
            "report": {
                "events": {
                    "data": [
                        {"timestamp": 90_000, "type": "cast", "sourceID": 5, "abilityGameID": RITUAL_OF_AWAKENING},
                        {"timestamp": 120_000, "type": "cast", "sourceID": 5, "abilityGameID": SOUL_TRANSFER},
                        {"timestamp": 150_000, "type": "cast", "sourceID": 5, "abilityGameID": SOUL_TRANSFER},
                    ],
                },
            },
        },
    }


def _phase_transitions() -> dict[str, object]:
    return {
        "reportData": {
            "report": {
                "fights": [
                    {
                        "id": FIGHT_ID,
                        "phaseTransitions": [
                            {"id": 1, "startTime": 0},
                            {"id": 2, "startTime": 110_000},
                            {"id": UNCOILING_TRANSITION, "startTime": 180_000},
                        ],
                    },
                ],
            },
        },
    }


class OrderedWarcraftlogsClient:
    """Serves a Nek'zali kill, with boss Casts and Phases finishing in a chosen order."""

    def __init__(self, *, boss_first: bool) -> None:
        self.boss_first = boss_first
        self.boss_loaded = asyncio.Event()
        self.phases_loaded = asyncio.Event()

    async def query(self, query: str) -> dict[str, object]:
        if "characterRankings" in query:
            return _ranking_payload()
        if "phaseTransitions" in query:
            if self.boss_first:
                await self.boss_loaded.wait()
            self.phases_loaded.set()
            return _phase_transitions()
        if str(RITUAL_OF_AWAKENING) in query:
            if not self.boss_first:
                await self.phases_loaded.wait()
            self.boss_loaded.set()
            return _boss_events()
        return {"reportData": {"report": {"events": {"data": []}, "fights": []}}}


@pytest.mark.parametrize("boss_first", [True, False])
def test_spec_ranking_phases_do_not_depend_on_load_order(boss_first: bool) -> None:
    """A spec-ranking Fight gets the same Phases whichever of the boss or the phases finishes first."""
    ranking = SpecRanking(
        game_version="retail",
        difficulty="mythic",
        spec_slug="paladin-holy",
        boss_slug=NEKZALI.full_name_slug,
        metric="hps",
    )

    asyncio.run(
        SpecRankingLoader(ranking, RETAIL).load(
            client=OrderedWarcraftlogsClient(boss_first=boss_first),
            limit=10,
        ),
    )

    fight = ranking.reports[0].fights[0]
    assert [(phase.phase_id, phase.timestamp) for phase in fight.phases] == KILL_PHASES


class _QuietWarcraftlogsClient:
    async def query(self, query: str) -> dict[str, object]:
        if "characterRankings" in query:
            return {"worldData": {"encounter": {"characterRankings": {"rankings": []}}}}
        return {"reportData": {"report": {"events": {"data": []}, "fights": []}}}


def test_spec_ranking_keeps_phases_when_process_phases_raises(caplog: pytest.LogCaptureFixture) -> None:
    """A boss phase correction that raises is logged and leaves the Fight's Phases as they were."""

    class ExplodingPhaseBoss(RaidBoss):
        id: int = 90641
        name: str = "Exploding Phase Boss"
        phase_type: RaidBoss.PhaseType = RaidBoss.PhaseType.DYNAMIC

        @override
        def process_phases(self, phases: list[Phase], casts: list[Cast]) -> list[Phase]:
            raise RuntimeError("phase correction failed")

    boss_type = ExplodingPhaseBoss()
    fight = Fight(
        fight_id=FIGHT_ID,
        start_time=datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC),
        phases=[Phase(ts=10_000, phase_id=2)],
        players=[
            Player(
                name="Healer",
                spec_slug="paladin-holy",
                casts=[Cast(spell_id=1, timestamp=1)],
            ),
        ],
        boss=Boss(boss_slug=boss_type.full_name_slug),
    )
    ranking = SpecRanking(
        game_version="retail",
        difficulty="mythic",
        spec_slug="paladin-holy",
        boss_slug=boss_type.full_name_slug,
        metric="hps",
        reports=[
            Report(
                report_id=REPORT_CODE,
                start_time=fight.start_time,
                fights=[fight],
            ),
        ],
    )

    with caplog.at_level(logging.ERROR, logger="Lorgs"):
        asyncio.run(
            SpecRankingLoader(ranking, game_version_with(game_data_with(bosses=[boss_type], specs=[GAME_DATA.get_spec("paladin-holy")]))).load(
                client=_QuietWarcraftlogsClient(), limit=10,
            ),
        )

    assert [(phase.phase_id, phase.timestamp) for phase in fight.phases] == [(2, 10_000)]
    assert "phase correction failed" in caplog.text


def test_spec_ranking_corrects_phases_loaded_after_the_boss_casts() -> None:
    """Phases loaded in this pass are corrected when the boss Casts were already loaded."""
    fight = Fight(
        fight_id=FIGHT_ID,
        start_time=datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC),
        players=[
            Player(
                name="Healer",
                spec_slug="paladin-holy",
                casts=[Cast(spell_id=1, timestamp=1)],
            ),
        ],
        boss=Boss(
            boss_slug=NEKZALI.full_name_slug,
            casts=[
                Cast(spell_id=RITUAL_OF_AWAKENING, timestamp=90_000),
                Cast(spell_id=SOUL_TRANSFER, timestamp=120_000),
                Cast(spell_id=SOUL_TRANSFER, timestamp=150_000),
            ],
        ),
    )
    ranking = SpecRanking(
        game_version="retail",
        difficulty="mythic",
        spec_slug="paladin-holy",
        boss_slug=NEKZALI.full_name_slug,
        metric="hps",
        reports=[
            Report(
                report_id=REPORT_CODE,
                start_time=fight.start_time,
                fights=[fight],
            ),
        ],
    )

    asyncio.run(SpecRankingLoader(ranking, RETAIL).load(client=_PhasesAlreadyHaveCastsClient(), limit=10))

    assert [(phase.phase_id, phase.timestamp) for phase in fight.phases] == KILL_PHASES


class _PhasesAlreadyHaveCastsClient:
    async def query(self, query: str) -> dict[str, object]:
        if "characterRankings" in query:
            return {"worldData": {"encounter": {"characterRankings": {"rankings": []}}}}
        if "phaseTransitions" in query:
            return _phase_transitions()
        return {"reportData": {"report": {"events": {"data": []}, "fights": []}}}


def test_user_report_corrects_phases_after_the_boss_loads() -> None:
    """A user report corrects Phases after the boss Casts finish loading."""
    fight = Fight(
        fight_id=FIGHT_ID,
        start_time=datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC),
        phases=[
            Phase(ts=110_000, phase_id=2),
            Phase(ts=180_000, phase_id=UNCOILING_TRANSITION),
        ],
        players=[Player(name="Healer", spec_slug="paladin-holy", source_id=10)],
        boss=Boss(boss_slug=NEKZALI.full_name_slug),
    )
    report = Report(
        report_id=REPORT_CODE,
        start_time=fight.start_time,
        fights=[fight],
    )

    asyncio.run(
        ReportLoader(report, GAME_DATA).load(
            client=_BossEventsClient(),
            fight_ids=[FIGHT_ID],
            load_boss=True,
        ),
    )

    assert [(phase.phase_id, phase.timestamp) for phase in fight.phases] == KILL_PHASES


class _BossEventsClient:
    async def query(self, query: str) -> dict[str, object]:
        if str(RITUAL_OF_AWAKENING) in query:
            return _boss_events()
        return {"reportData": {"report": {"events": {"data": []}, "fights": []}}}
