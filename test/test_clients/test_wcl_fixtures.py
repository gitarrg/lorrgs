"""Real Warcraft Logs responses parse through the typed client models.

Pydantic ignores unknown keys and most fields have defaults, so a renamed field would
silently fall back to its default. Each test therefore asserts the values the fixture holds.
"""

from lorgs.clients import wcl
from test.helpers import load_fixture


def test_character_rankings() -> None:
    query = wcl.Query.model_validate(load_fixture("spec_rankings_1.json"))

    rankings = query.world_data.encounter.characterRankings
    assert rankings.page == 1
    assert rankings.hasMorePages is True
    assert rankings.count == 100
    assert len(rankings.rankings) > 0

    first = rankings.rankings[0]
    assert first.name
    assert first.class_ == "Paladin"
    assert first.spec == "Holy"
    assert first.amount > 0
    assert first.duration > 0
    assert first.startTime.year == 2021
    assert first.report.code == "Q7jC6zbftX1ahdVR"
    assert first.report.fightID == 5
    assert first.report.startTime.year == 2021


def test_report_overview() -> None:
    query = wcl.Query.model_validate(load_fixture("report_masterData_1.json"))

    report = query.report
    assert report.title == "Sepulcher of the First Ones"
    assert report.zone.id == 29
    assert report.zone.name == "Sepulcher of the First Ones"
    assert report.owner.name == "Arrg"
    assert report.startTime.year == 2022
    assert report.endTime > report.startTime

    assert len(report.fights) > 1
    wipe, kill = report.fights[0], report.fights[1]
    assert (wipe.id, wipe.encounterID, wipe.kill, wipe.fightPercentage) == (1, 2553, False, 73.9)
    assert (kill.id, kill.name, kill.startTime, kill.endTime, kill.kill) == (
        2,
        "Artificer Xy'mox",
        271703,
        493690,
        True,
    )

    assert report.masterData is not None
    assert len(report.masterData.actors) > 0
    actor = report.masterData.actors[0]
    assert actor.id
    assert actor.name
    assert actor.type
    assert actor.subType


def test_report_events() -> None:
    query = wcl.Query.model_validate(load_fixture("report_data_1.json"))

    events = query.report.events
    assert len(events) > 0
    first = events[0]
    assert first.timestamp == 10222511
    assert first.type == "cast"
    assert first.sourceID == 4
    assert first.targetID == -1
    assert first.abilityGameID == 498
    assert first.fight == 34


def test_report_summary() -> None:
    query = wcl.Query.model_validate(load_fixture("fight_summary_1.json"))

    summary = query.report.summary
    assert summary is not None
    assert summary.totalTime == 728598
    assert summary.itemLevel > 0
    assert len(summary.composition) > 0

    first = summary.composition[0]
    assert first.name == "Blackric"
    assert first.id == 6
    assert first.type == "Hunter"
    assert len(first.specs) > 0
    assert first.specs[0].spec
    assert first.specs[0].role
