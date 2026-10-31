"""`load_fights` through its interface, against a fake Warcraft Logs client."""

import asyncio
import datetime

from lorgs.loaders.fights_loader import FightPlan, load_fights
from lorgs.models.game_data import GameData
from lorgs.models.warcraftlogs_cast import Cast
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_player import Player
from lorgs.models.warcraftlogs_report import Report
from lorgs.models.wow_spec import WowSpec


START = datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC)


class FakeClient:
    """Answers every query with an empty report, except for the fight ids in `failing`."""

    def __init__(self, failing: tuple[int, ...] = ()) -> None:
        self.queries: list[str] = []
        self.failing = failing

    async def query(self, query: str) -> dict[str, object]:
        self.queries.append(query)
        if any(f"fightIDs: {fight_id}" in query or f"fightIDs:{fight_id}" in query for fight_id in self.failing):
            raise RuntimeError("boom")
        return {"reportData": {"report": {"events": {"data": []}, "fights": []}}}


def _report(spec: WowSpec, *, loaded: bool, fight_ids=(1,)) -> Report:
    fights = []
    for fight_id in fight_ids:
        players = []
        if loaded:
            players = [
                Player(source_id=sid, name=f"P{sid}", spec_slug=spec.full_name_slug, casts=[Cast(spell_id=1, timestamp=1)])
                for sid in (1, 2)
            ]
        fights.append(Fight(fight_id=fight_id, start_time=START, players=players))
    report = Report(report_id="abc", start_time=START, fights=fights)
    report.post_init()
    return report


def _run(plans: list[FightPlan], game_data: GameData, client: FakeClient):
    return asyncio.run(load_fights(plans, game_data, client=client))


def test_loaded_fights_cause_no_queries(spec: WowSpec, game_data: GameData) -> None:
    report = _report(spec, loaded=True)
    client = FakeClient()

    failures = _run([FightPlan(report.fights[0], players="all")], game_data, client)

    assert failures == []
    assert client.queries == []


def test_missing_players_are_loaded_by_source_id(spec: WowSpec, game_data: GameData) -> None:
    report = _report(spec, loaded=True)
    fight = report.fights[0]
    fight.players[1].casts = []
    client = FakeClient()

    _run([FightPlan(fight, players=[2])], game_data, client)

    assert len(client.queries) == 1  # only player 2, player 1 is not picked


def test_no_players_loads_nothing(spec: WowSpec, game_data: GameData) -> None:
    report = _report(spec, loaded=True)
    report.fights[0].players[0].casts = []
    client = FakeClient()

    _run([FightPlan(report.fights[0])], game_data, client)

    assert client.queries == []


def test_missing_summary_is_queried(spec: WowSpec, game_data: GameData) -> None:
    report = _report(spec, loaded=False)
    client = FakeClient()

    _run([FightPlan(report.fights[0])], game_data, client)

    assert len(client.queries) == 1
    assert "Summary" in client.queries[0]


def test_failing_fight_is_returned_and_others_still_load(spec: WowSpec, game_data: GameData) -> None:
    report = _report(spec, loaded=True, fight_ids=(1, 2))
    good, bad = report.fights
    good.players[0].casts = []
    bad.players[0].casts = []
    client = FakeClient(failing=(2,))

    failures = _run([FightPlan(bad, players="all"), FightPlan(good, players="all")], game_data, client)

    assert [(f.fight.fight_id, type(f.error)) for f in failures] == [(2, RuntimeError)]
    assert any("fightIDs: 1" in q or "fightIDs:1" in q for q in client.queries)
