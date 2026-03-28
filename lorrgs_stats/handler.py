import asyncio
import os
import datetime

import aiohttp

from lorgs.clients import wcl
from lorgs.logger import timeit

GRAFANA_URL = os.getenv("GRAFANA_URL") or ""
GRAFANA_APIKEY = os.getenv("GRAFANA_APIKEY") or ""

loop = asyncio.new_event_loop()


@timeit
async def send_metric(prefix: str, **values: int) -> None:
    headers = {"Authorization": f"Bearer {GRAFANA_APIKEY}"}

    data = [
        {
            "name": f"{prefix}.{name}",
            "value": value,
            "interval": 10000,
            "time": int(datetime.datetime.now().timestamp()),
        }
        for name, value in values.items()
    ]
    # result = requests.post(GRAFANA_URL, json=data, headers=headers)
    # print(result, result.text)

    async with aiohttp.ClientSession() as session:
        async with session.post(url=GRAFANA_URL, json=data, headers=headers) as resp:
            print(resp)


async def get_rate_info() -> dict[str, int]:
    wcl_client = wcl.WarcraftlogsClient()
    query = """
        rateLimitData
        {
            pointsSpentThisHour
            limitPerHour
            pointsResetIn
        }
        """

    result = await wcl_client.query(query)
    await wcl_client.session.close()
    return result.get("rateLimitData") or {}


async def main() -> None:
    rate_info = await get_rate_info()
    print(rate_info)

    await send_metric(prefix="wcl.rate_info", **rate_info)


def handler(event=None, context=None) -> None:
    loop.run_until_complete(main())


if __name__ == "__main__":
    handler()
