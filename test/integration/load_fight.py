import asyncio
import datetime

import dotenv

dotenv.load_dotenv()

from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models import warcraftlogs_report
from lorgs import data


def create_fight() -> Fight:
    """Create an Example Fight Instance."""
    report = warcraftlogs_report.Report(
        report_id="tZVAxLYg7kTz1PBm", start_time=datetime.datetime.fromtimestamp(1666891263596 / 1000)
    )

    fight = Fight(
        fight_id=2,
        boss_id=2553,
        start_time=report.start_time + datetime.timedelta(milliseconds=271703),
        duration=(493690 - 271703),
    )
    fight.report = report
    return fight


async def load_fight_overview() -> None:
    """Load a the fight Overview."""
    fight = create_fight()

    q = fight.get_query()
    print(q)
    # fight.client.query(q)
    await fight.load()

    print(fight.players)
    print(fight.as_dict())
    return
    return


async def main():
    await load_fight_overview()
    # await load_casts()


if __name__ == "__main__":
    asyncio.run(main())
