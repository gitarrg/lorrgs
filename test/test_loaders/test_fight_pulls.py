import datetime

from lorgs.clients import wcl
from lorgs.loaders.fight_loader import FightLoader
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.dungeon import Dungeon
from lorgs.models.warcraftlogs_report import Report
from test.helpers import game_data_with


def test_dungeon_pulls_are_relative_to_the_run():
    game_data = game_data_with(dungeons=[Dungeon(id=500, name="Test Dungeon")])
    report = Report(report_id="abc", start_time=datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC))
    fight_data = wcl.ReportFight.model_validate(
        {
            "id": 3,
            "encounterID": 500,
            "difficulty": RaidDifficulty.DUNGEON.value,
            "startTime": 10_000,
            "endTime": 70_000,
            "dungeonPulls": [
                {"id": 1, "encounterID": 0, "name": "Trash", "startTime": 10_000, "endTime": 25_000},
                {"id": 2, "encounterID": 900, "name": "Big Boss", "startTime": 30_000.0, "endTime": 60_000.0},
            ],
        }
    )

    fight = FightLoader.fight_from_wcl_fight(fight_data, report=report, game_data=game_data)

    assert fight is not None
    assert [pull.model_dump() for pull in fight.pulls] == [
        {"start": 0, "end": 15_000, "boss": None},
        {"start": 20_000, "end": 50_000, "boss": "Big Boss"},
    ]
    assert fight.as_dict(game_data)["pulls"][1]["boss"] == "Big Boss"
