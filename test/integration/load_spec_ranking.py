
import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position
import asyncio


from lorgs import data  # pylint: disable=unused-import
from lorgs import db   # pylint: disable=unused-import

from lorgs.models.warcraftlogs_ranking import SpecRanking


async def test__load_rankings():
    spec_ranking = SpecRanking.get_or_create(spec_slug="paladin-holy", boss_slug="painsmith-raznal")

    await spec_ranking.load(limit=15)
    spec_ranking.save()


async def main():
    await test__load_rankings()


if __name__ == "__main__":
    asyncio.run(main())
