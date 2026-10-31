import dotenv


dotenv.load_dotenv()  # pylint: disable=wrong-import-position
import asyncio

from lorgs.data import RETAIL
from lorgs.data.retail import GAME_DATA
from lorgs.loaders.comp_ranking import CompRankingLoader
from lorgs.models import warcraftlogs_comp_ranking


async def test__load_rankings(boss_slug: str, page=1, clear=False) -> None:
    ################################
    # get comp ranking object
    ranking = warcraftlogs_comp_ranking.CompRanking.get_or_create(game_version=RETAIL.name, boss_slug=boss_slug)
    if not GAME_DATA.get_boss(full_name_slug=boss_slug):
        return False, "invalid boss"

    ################################
    # load and save
    await CompRankingLoader(ranking, RETAIL, page=page, clear_old=clear).load()
    ranking.save()
    return True, "done"


async def test__print_rankings(boss_slug: str) -> None:
    comp_ranking = warcraftlogs_comp_ranking.CompRanking.get_or_create(game_version=RETAIL.name, boss_slug=boss_slug)
    comp_ranking.sort_reports()

    for report in comp_ranking.reports:
        for fight in report.fights:
            print(fight.deaths, fight.damage_taken, fight.duration)

    comp_ranking.save()


async def main() -> None:
    boss_slug = "sikran-captain-of-the-sureki"
    await test__load_rankings(boss_slug)


if __name__ == "__main__":
    asyncio.run(main())
