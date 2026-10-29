import asyncio

import dotenv

from lorgs import data  # pylint: disable=unused-import
from lorgs.models.warcraftlogs_ranking import SpecRanking


dotenv.load_dotenv()

TEMP_FILE = "/mnt/d/tmp.json"


async def test__load_rankings():
    spec_ranking = SpecRanking.get_or_create(
        spec_slug="evoker-augmentation",
        boss_slug="kazzara-the-hellforged",
        difficulty="heroic",
        metric="dps",
    )

    for player in spec_ranking.players:
        print(player.name)
        for cast in player.casts:
            print("...", cast)
        # return
    # return

    await spec_ranking.load(limit=5, clear_old=True)
    spec_ranking.save()
    # return

    # print(spec_ranking)
    # print(spec_ranking.dict())
    # spec_ranking.save()
    # return

    ##############
    # Additional Formatting
    # fights = spec_ranking.fights or []
    # result = {
    #     "updated": int(spec_ranking.updated.timestamp()),
    #     "difficulty": difficulty,
    #     "metric": metric,
    # }
    with open(TEMP_FILE, "w") as f:
        f.write(spec_ranking.model_dump_json(exclude_unset=True, indent=4))
        # json.dump(, f, indent=4)


async def test__load_from_disk():
    spec_ranking = SpecRanking.parse_file(TEMP_FILE)
    spec_ranking.post_init()

    for report in spec_ranking.reports:
        print("R", report)
        for fight in report.fights:
            print("\tF", fight)
            for player in fight.players:
                print("\t\tP:", player)
                print(player.get_query())
            # print(fight.dict())
    # print(spec_ranking)
    # print(spec_ranking.dict())


async def test__load_from_db():
    spec_ranking = SpecRanking.get_or_create(
        spec_slug="druid-restoration",
        boss_slug="lords-of-dread",
        difficulty="mythic",
        metric="hps",
    )
    # print(spec_ranking)
    await spec_ranking.load(limit=5, clear_old=True)
    spec_ranking.save()
    # print(spec_ranking)
    # with open(TEMP_FILE, "w") as f:
    #     f.write(spec_ranking.json(exclude_unset=True, indent=4))
    #     # json.dump(, f, indent=4)


async def main():
    # pass
    await test__load_rankings()
    # await test__load_from_disk()
    # await test__load_from_db()


if __name__ == "__main__":
    # asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    """
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
    """
