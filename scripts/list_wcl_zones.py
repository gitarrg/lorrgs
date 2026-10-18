#!/usr/bin/env -S PYTHONPATH=. uv run --env-file=.env
"""List Warcraft Logs zones and their encounters.

Looks up ``RaidZone(id=...)`` and boss ids. Kith'ix (3513) is in zone 53.

    scripts/list_wcl_zones.py
    scripts/list_wcl_zones.py kith

"""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import argparse
import asyncio

# IMPORT LOCAL LIBRARIES
from lorgs.clients.wcl import WarcraftlogsClient


QUERY = """
worldData {
    expansions {
        name
        zones {
            id
            name
            encounters {
                id
                name
            }
        }
    }
}
"""


def _matches(text: str, needles: list[str]) -> bool:
    lowered = text.lower()
    return any(needle in lowered for needle in needles)


async def main() -> None:
    parser = argparse.ArgumentParser(description="List Warcraft Logs zones and encounters.")
    parser.add_argument(
        "filter",
        nargs="*",
        help="only print zones or encounters whose name contains one of these substrings",
    )
    args = parser.parse_args()
    needles = [part.lower() for part in args.filter]

    client = WarcraftlogsClient()
    try:
        data = await client.query(QUERY)
    finally:
        await client.session.close()

    for expansion in data["worldData"]["expansions"] or []:
        printed_expansion = False
        for zone in expansion.get("zones") or []:
            encounters = zone.get("encounters") or []
            zone_hit = not needles or _matches(zone.get("name") or "", needles)
            shown = encounters if zone_hit else [enc for enc in encounters if _matches(enc.get("name") or "", needles)]
            if needles and not shown:
                continue

            if not printed_expansion:
                print(expansion["name"])
                printed_expansion = True

            print(f"  {zone['id']:<4}  {zone['name']}")
            for enc in shown:
                print(f"    {enc['id']:<6}  {enc['name']}")


if __name__ == "__main__":
    asyncio.run(main())
