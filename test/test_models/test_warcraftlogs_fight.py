import datetime
import unittest

import pytest

from lorgs.clients import wcl
from lorgs.loaders.fight_loader import FightLoader
from lorgs.loaders.fight_phases import FightPhasesLoader
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.warcraftlogs_boss import Boss
from lorgs.models.warcraftlogs_comp_ranking import get_composition
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_report import Report

from ..helpers import load_fixture


# 21s after the report starts. A report-time event at 25s is 4s into the fight.
REPORT_START = datetime.datetime.fromtimestamp(100, datetime.UTC)
FIGHT_START = datetime.datetime.fromtimestamp(121, datetime.UTC)


def _fight(**kwargs) -> Fight:
    values = {
        "fight_id": 5,
        "start_time": datetime.datetime.fromtimestamp(101, datetime.UTC),
        "duration": 3000,
    }
    values.update(kwargs)
    return Fight(**values)


class TestFight(unittest.TestCase):
    def setUp(self):
        self.fight = _fight()
        self.fight.report = unittest.mock.MagicMock()
        self.fight.report.start_time = datetime.datetime.fromtimestamp(100, datetime.UTC)
        self.fight.report.report_id = "REPORT_ID"

    def test_start_time_rel(self):
        self.fight.report.start_time = datetime.datetime.fromtimestamp(100, datetime.UTC)
        self.fight.start_time = datetime.datetime.fromtimestamp(121, datetime.UTC)
        assert self.fight.start_time_rel == 21000

    def test_end_time_rel(self):
        self.fight.report.start_time = datetime.datetime.fromtimestamp(100, datetime.UTC)
        self.fight.start_time = datetime.datetime.fromtimestamp(120, datetime.UTC)
        self.fight.duration = 600 * 1000
        assert self.fight.end_time_rel == 620 * 1000

    def test_table_query_args(self):
        result = self.fight.table_query_args
        assert result == "fightIDs: 5, startTime: 1000, endTime: 4000"


class TestFightProcessPlayers(unittest.TestCase):
    def setUp(self):
        self.fight = _fight()
        # Deaths convert through the Fight, which needs its Report.
        self.fight.report = Report(report_id="REPORT_ID", start_time=self.fight.start_time)
        self.loader = FightLoader(self.fight)

    def test_empty(self):
        self.loader._process_summary(wcl.ReportSummary())
        assert self.fight.players == []


def _fight_in_report(**kwargs) -> Fight:
    fight = _fight(start_time=FIGHT_START, **kwargs)
    fight.report = Report(report_id="REPORT_ID", start_time=REPORT_START)
    return fight


def test_report_time_converts_to_milliseconds_since_the_fight_started() -> None:
    fight = _fight_in_report()

    assert fight.to_fight_time(25_000) == 4_000


def test_converting_without_a_report_raises() -> None:
    fight = _fight(start_time=FIGHT_START)

    with pytest.raises(ValueError, match="Missing Parent Report"):
        fight.to_fight_time(25_000)


def _fight_with_phase_boss() -> tuple[Fight, RaidBoss]:
    # The boss is only findable while this instance is still referenced.
    raid_boss = RaidBoss(id=990072, name="Conversion Test Boss")
    fight = _fight_in_report()
    fight.boss = Boss.from_raid_boss(raid_boss)
    return fight, raid_boss


def test_phases_are_fight_relative() -> None:
    fight, _raid_boss = _fight_with_phase_boss()

    FightPhasesLoader(fight).process_phase_transitions([
        wcl.PhaseTransition(id=2, startTime=25_000),
    ])

    assert fight.phases[0].timestamp == 4_000


def test_phase_loading_leaves_its_input_unchanged() -> None:
    fight, _raid_boss = _fight_with_phase_boss()
    transition = wcl.PhaseTransition(id=2, startTime=25_000)

    FightPhasesLoader(fight).process_phase_transitions([transition])

    assert transition.startTime == 25_000


def test_phases_raise_when_the_fight_has_no_report() -> None:
    fight, _raid_boss = _fight_with_phase_boss()
    fight.report = None
    transition = wcl.PhaseTransition(id=2, startTime=25_000)

    with pytest.raises(ValueError, match="Missing Parent Report"):
        FightPhasesLoader(fight).process_phase_transitions([transition])

    assert transition.startTime == 25_000
    assert fight.phases == []
