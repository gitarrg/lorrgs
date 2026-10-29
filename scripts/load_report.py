#!/usr/bin/env -S PYTHONPATH=. uv run --env-file=.env
"""Load a Report given by an URL."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import argparse
import asyncio
import re
import typing
from urllib.parse import parse_qs, urlparse

import pydantic

# IMPORT LOCAL LIBRARIES
from lorgs import (
    data,  # ruff: ignore[unused-import]
    utils,
)
from lorgs.data import GAME_DATA
from lorgs.loaders.report_loader import ReportLoader
from lorgs.models.warcraftlogs_user_report import UserReport


if typing.TYPE_CHECKING:
    from lorgs.models.warcraftlogs_actor import BaseActor
    from lorgs.models.warcraftlogs_fight import Fight


def print_actor(actor: BaseActor) -> None:
    casts = actor.casts if actor else []
    if not casts:
        print("  (none)")
        return

    for cast in casts:
        spell = GAME_DATA.get_spell(cast.spell_id)
        name = spell.name if spell else ""
        timestamp = utils.format_time(cast.timestamp)
        print(f"  {timestamp:>7}  {cast.event_type:<12}  {cast.spell_id:<7}  {name}")


def print_fight(fight: Fight) -> None:
    """Print loaded events and phases for one fight."""
    print(f"\nFight {fight.fight_id}")

    print("phases:")
    if fight.phases:
        for phase in fight.phases:
            timestamp = utils.format_time(phase.timestamp)
            print(f"  {timestamp:>7}  id={phase.phase_id}  {phase.name}")
    else:
        print("  (none)")

    print("boss events:")
    if boss := fight.boss:
        print(f"  boss: {boss.raid_boss.name}")
        print_actor(fight.boss)
    else:
        print("  (none)")

    print("player events:")
    for player in fight.players:
        print(f"  {player.source_id} name={player.name=} | spec={player.spec.full_name_slug}")
        print_actor(player)


class WarcraftReport(pydantic.BaseModel):
    """Small Helper Class to Hold Report Information."""

    report_id: str
    fight_ids: list[int] = []
    player_ids: list[int] = []

    @classmethod
    def from_url(cls, url: str):
        report_match = re.search(r"reports/(\w{16})", url)
        report_id = report_match.group(1) if report_match else ""

        query_params = parse_qs(urlparse(url).query)
        fight_ids = [int(v) for v in query_params.get("fight", [-1])]
        player_ids = [int(v) for v in query_params.get("source", [-1])]

        return cls(
            report_id=report_id,
            fight_ids=fight_ids,
            player_ids=player_ids,
        )

    def as_lorrgs_url(self) -> str:

        def to_str(items: list, sep: str = ".") -> str:
            return sep.join(str(item) for item in items)

        fight_ids_str = to_str(self.fight_ids)
        player_ids_str = to_str(self.player_ids)
        return f"http://localhost:9001/user_report/{self.report_id}?fight={fight_ids_str}&player={player_ids_str}"

    async def load(
        self,
        *,
        print_events: bool = False,
        save_report: bool = True,
    ) -> None:

        # Load
        user_report = UserReport.get_or_create(report_id=self.report_id, create=True)
        user_report.fights = []  # force reload

        loader = ReportLoader(report=user_report)
        await loader.load(
            fight_ids=self.fight_ids,
            player_ids=self.player_ids,
            load_boss=True,
        )

        if print_events:
            fights = user_report.get_fights(*self.fight_ids)
            if not fights:
                print("No fights loaded.")
                return
            for fight in fights:
                print_fight(fight)
            return

        if not save_report:
            user_report.save()

        print(self.as_lorrgs_url())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load a Warcraft Logs report.")
    parser.add_argument("url", nargs="?", type=str, help="Full Warcraft Logs report URL")
    parser.add_argument("--report", type=str, help="Report ID")
    parser.add_argument("--fight", type=int, nargs="+", help="Fight IDs", default=[-1])
    parser.add_argument("--source", type=int, nargs="+", help="Source (Player) IDs", default=[-1])
    parser.add_argument(
        "--print-events",
        action="store_true",
        help="Print events and phases without saving",
    )
    parser.add_argument(
        "--save-report",
        action="store_true",
        help="Save the report to the database",
    )

    args = parser.parse_args()

    if args.url:
        report = WarcraftReport.from_url(args.url)
    elif args.report:
        report = WarcraftReport(
            report_id=args.report,
            fight_ids=args.fight,
            player_ids=args.source,
        )
    else:
        parser.error("Either --url or --report must be provided.")

    print("--- Loading ----")
    print(report)
    asyncio.run(
        report.load(
            print_events=args.print_events,
            save_report=args.save_report,
        ),
    )
