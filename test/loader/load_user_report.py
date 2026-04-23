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
            print(f"F={fight.fight_id} | len(players)={len(fight.players)}")
            for player in fight.players:
                if player.casts:
                    print(f"\t F={fight.fight_id} | id={player.source_id} name={player.name} casts={len(player.casts)}")
                # for cast in player.casts:
                #     print("\t", cast)

    fight_ids = [46, 47, 51]
    player_ids = [5, 14, 43, 58]
    report = UserReport.get_or_create(report_id="pzRXNvHVG8qtk9ch")
    # print_info(report)

    loader = ReportLoader(report=report)
    await loader.load(
        fight_ids=fight_ids,
        player_ids=player_ids,
        load_boss=True,
    )
    report.save()
    print_info(report)


    host = "http://localhost:9001"
    figths_ids_str = ".".join([str(f) for f in fight_ids])
    players_ids_str = ".".join([str(p) for p in player_ids])
    url = f"{host}/user_report/pzRXNvHVG8qtk9ch?fight={figths_ids_str}&player={players_ids_str}"
    print(url)



if __name__ == "__main__":
    asyncio.run(main())
