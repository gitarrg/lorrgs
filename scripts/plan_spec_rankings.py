#!/usr/bin/env -S PYTHONPATH=. uv run
"""Run the Refresh Planner locally: log the Spec Rankings it would refresh this hour, oldest first.

A dry run: nothing is queued. Reads S3 (`LastModified`) and Warcraft Logs (`rateLimitData`).
"""

# IMPORT STANDARD LIBRARIES
import argparse
import asyncio

# IMPORT LOCAL LIBRARIES
from lorgs.clients.wcl import WarcraftlogsClient
from lorrgs_sqs.task_handlers import plan_spec_rankings


async def main() -> None:
    try:
        print(await plan_spec_rankings.plan_spec_rankings())
    finally:
        await WarcraftlogsClient.get_instance().session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    asyncio.run(main())
