#!/usr/bin/env -S PYTHONPATH=. uv run
"""Run the Refresh Planner locally: log the Spec Rankings it would refresh this hour, oldest first.

A dry run unless `--queue` is passed. Reads S3 (`LastModified`) and Warcraft Logs (`rateLimitData`).
"""

# IMPORT STANDARD LIBRARIES
import argparse
import asyncio

# IMPORT LOCAL LIBRARIES
from lorgs.clients.wcl import WarcraftlogsClient
from lorrgs_sqs.task_handlers import plan_spec_rankings


async def main(*, dry_run: bool) -> None:
    try:
        print(await plan_spec_rankings.plan_spec_rankings(dry_run=dry_run))
    finally:
        await WarcraftlogsClient.get_instance().session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", action="store_true", help="queue the planned Refreshes instead of only logging them")
    args = parser.parse_args()
    asyncio.run(main(dry_run=not args.queue))
