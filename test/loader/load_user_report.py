



"""Load a Spec Ranking from WarcraftLogs.

>>> PYTHONPATH=. uv --env-file=.env  run tmp.py

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


    fight_ids = [10, 12, 32]
    player_ids = [16, 19]
    report = UserReport.get_or_create(report_id="XQpJLB38k49ZP1Wz")
    print_info(report)

    loader = ReportLoader(report=report)
    await loader.load(
        fight_ids=fight_ids,
        player_ids=player_ids,
    )
    report.save()

    print_info(report)



if __name__ == "__main__":
    asyncio.run(main())
