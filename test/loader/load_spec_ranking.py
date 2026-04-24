"""Load a Spec Ranking from WarcraftLogs.

>>> PYTHONPATH=. uv run --env-file=.env  test/loader/load_spec_ranking.py

"""
import asyncio

from lorgs.data import *  # noqa: F403
from lorgs.loaders.spec_ranking import SpecRankingLoader
from lorgs.models.warcraftlogs_ranking import SpecRanking


async def main():

    # ranking = SpecRanking.get_or_create(
    #     spec_slug="hunter-survival",
    #     boss_slug="vorasius",
    #     difficulty="heroic",
    #     metric="hps",
    # )

    ranking = SpecRanking.get_or_create(
        spec_slug="druid-restoration",
        boss_slug="beloren-child-of-alar",
        difficulty="mythic",
        metric="hps",
    )

    for report in ranking.reports:
        print("OLD", report)
        """
        for fight in report.fights:
            print("F", fight)

            if fight.boss:
                print("FB", fight.boss)
                for cast in fight.boss.casts:
                    print("FBC", cast.spell)

            for player in fight.players:
                print("FP", player.name)
                for cast in player.casts:
                    print("FPC", cast.spell)
        """

    loader = SpecRankingLoader(ranking=ranking)
    await loader.load(
        limit=5,
        clear_old=False,
    )
    # ranking.save()


if __name__ == "__main__":
    asyncio.run(main())
