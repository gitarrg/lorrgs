"""Load a Spec Ranking from WarcraftLogs.

>>> PYTHONPATH=. uv run --env-file=.env  test/loader/load_user_report.py

"""
import asyncio

from lorgs.data import *  # noqa: F403
from lorgs.loaders.report_loader import ReportLoader
from lorgs.models.warcraftlogs_user_report import UserReport


async def main():

    def print_info(report: UserReport):
        print("num fights:", len(report.fights))
        for fight in report.fights:
            for player in fight.players:
                if player.casts:
                    print(f"\t F={fight.fight_id} | id={player.source_id} name={player.name} casts={len(player.casts)}")
                # for cast in player.casts:
                #     print("\t", cast)

    fight_ids = [41, 42]
    player_ids = [5, 14, 43, 58]
    report = UserReport.get_or_create(report_id="pzRXNvHVG8qtk9ch")
    print_info(report)

    loader = ReportLoader(report=report)
    await loader.load(
        fight_ids=fight_ids,
        player_ids=player_ids,
        load_boss=True,
    )
    report.save()

    print_info(report)



if __name__ == "__main__":
    asyncio.run(main())
