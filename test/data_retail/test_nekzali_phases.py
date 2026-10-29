"""Boss-specific Phases are corrected by the Phase load, from the phase Casts it fetches itself."""

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
from lorgs.clients import wcl
from lorgs.loaders.fight_loader import FightLoader
from lorgs.loaders.fight_phases import FightPhasesLoader
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
    """Loading the boss does not change Phases. The Phase load corrects them."""
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


def _phases_and_casts() -> dict[str, object]:
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


class NekzaliWarcraftlogsClient:
    """Serves a Nek'zali kill. Only the Phase query returns the phase Casts; the boss load gets nothing."""

    def __init__(self) -> None:
        self.queries: list[str] = []

    async def query(self, query: str) -> dict[str, object]:
        self.queries.append(query)
        if "characterRankings" in query:
            return _ranking_payload()
        if "phaseTransitions" in query:
            return _phases_and_casts()
        return {"reportData": {"report": {"events": {"data": []}, "fights": []}}}


def _nekzali_fight(**kwargs: object) -> Fight:
    fight = Fight(
        fight_id=FIGHT_ID,
        start_time=datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC),
        boss=Boss(boss_slug=NEKZALI.full_name_slug),
        **kwargs,
    )
    Report(report_id=REPORT_CODE, start_time=fight.start_time, fights=[fight]).post_init()
    return fight


def test_phase_query_fetches_the_phase_casts() -> None:
    """Nek'zali's Phase query asks for its phase Casts next to the transitions."""
    query = FightPhasesLoader(_nekzali_fight(), GAME_DATA).get_query()

    events_query = query.split("events(")[1]
    assert "phaseTransitions" in query
    assert str(RITUAL_OF_AWAKENING) in events_query
    assert str(SOUL_TRANSFER) in events_query


def test_phase_query_of_other_bosses_has_no_events() -> None:
    """A boss without phase spells only asks for the transitions."""
    boss_type = RaidBoss(id=90065, name="Plain Phase Boss", phase_type=RaidBoss.PhaseType.DYNAMIC)
    fight = _nekzali_fight()
    fight.boss = Boss(boss_slug=boss_type.full_name_slug)
    game_data = game_data_with(bosses=[boss_type])

    query = FightPhasesLoader(fight, game_data).get_query()

    assert "phaseTransitions" in query
    assert "events" not in query


def test_phase_loader_corrects_phases_from_its_own_casts() -> None:
    """One Phase load is enough: the transitions and the phase Casts come back together."""
    fight = _nekzali_fight()
    client = NekzaliWarcraftlogsClient()

    asyncio.run(FightPhasesLoader(fight, GAME_DATA).load(client=client))

    assert len(client.queries) == 1
    assert [(phase.phase_id, phase.timestamp) for phase in fight.phases] == KILL_PHASES


def test_phase_loader_keeps_phases_when_process_phases_raises(caplog: pytest.LogCaptureFixture) -> None:
    """A boss phase correction that raises is logged and the Fight keeps the Phases from the transitions."""

    class ExplodingPhaseBoss(RaidBoss):
        id: int = 90641
        name: str = "Exploding Phase Boss"
        phase_type: RaidBoss.PhaseType = RaidBoss.PhaseType.DYNAMIC

        @override
        def process_phases(self, phases: list[Phase], casts: list[Cast]) -> list[Phase]:
            raise RuntimeError("phase correction failed")

    boss_type = ExplodingPhaseBoss()
    fight = _nekzali_fight()
    fight.boss = Boss(boss_slug=boss_type.full_name_slug)

    with caplog.at_level(logging.ERROR, logger="Lorgs"):
        asyncio.run(
            FightPhasesLoader(fight, game_data_with(bosses=[boss_type])).load(client=NekzaliWarcraftlogsClient()),
        )

    assert [(phase.phase_id, phase.timestamp) for phase in fight.phases] == [
        (2, 110_000),
        (UNCOILING_TRANSITION, 180_000),
    ]
    assert "phase correction failed" in caplog.text


def test_report_overview_leaves_nekzali_phases_to_the_phase_query() -> None:
    """The overview has no Casts, so it does not set Nek'zali's Phases."""
    report = Report(report_id=REPORT_CODE, start_time=datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC))
    fight_data = wcl.ReportFight(
        id=FIGHT_ID,
        encounterID=NEKZALI.id,
        startTime=0,
        endTime=300_000,
        difficulty=5,
        phaseTransitions=[wcl.PhaseTransition(id=UNCOILING_TRANSITION, startTime=180_000)],
    )

    fight = FightLoader.fight_from_wcl_fight(fight_data, report=report, game_data=GAME_DATA)

    assert fight is not None
    assert fight.phases == []
    assert FightPhasesLoader(fight, GAME_DATA).needs_load()


def test_spec_ranking_corrects_every_nekzali_fight() -> None:
    """A spec-ranking Fight gets corrected Phases from the Phase load alone."""
    ranking = SpecRanking(
        game_version="retail",
        difficulty="mythic",
        spec_slug="paladin-holy",
        boss_slug=NEKZALI.full_name_slug,
        metric="hps",
    )

    asyncio.run(SpecRankingLoader(ranking, RETAIL).load(client=NekzaliWarcraftlogsClient(), limit=10))

    fight = ranking.reports[0].fights[0]
    assert [(phase.phase_id, phase.timestamp) for phase in fight.phases] == KILL_PHASES


def test_user_report_fight_load_corrects_nekzali_phases() -> None:
    """A User Report Fight gets corrected Phases from the Fight load, without an extra request."""
    fight = _nekzali_fight()
    client = NekzaliWarcraftlogsClient()

    asyncio.run(ReportLoader(fight.report, GAME_DATA).load(client=client, fight_ids=[FIGHT_ID], load_boss=True))

    assert [(phase.phase_id, phase.timestamp) for phase in fight.phases] == KILL_PHASES
    assert sum("phaseTransitions" in query for query in client.queries) == 1
