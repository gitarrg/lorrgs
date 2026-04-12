"""Load a Spec Ranking from WarcraftLogs.

>>> PYTHONPATH=. uv --env-file=.env  run tmp.py

"""
import asyncio

from lorgs.data import *  # noqa: F403
from lorgs.loaders.report_overview_loader import ReportOverviewLoader
from lorgs.models.warcraftlogs_report import Report


async def main():


    report = Report(report_id="XQpJLB38k49ZP1Wz")

    loader = ReportOverviewLoader(report=report)
    await loader.load()


if __name__ == "__main__":
    asyncio.run(main())
