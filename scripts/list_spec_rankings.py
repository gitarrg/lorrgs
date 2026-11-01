#!/usr/bin/env -S PYTHONPATH=. uv run
"""List the stored Spec Rankings of a Game Version's current season, stalest first.

Reads S3's `LastModified` from the object listing instead of downloading each ranking.
"""

# IMPORT STANDARD LIBRARIES
import argparse
import time

# IMPORT LOCAL LIBRARIES
from lorgs.data import GAME_VERSIONS
from lorgs.models.base.s3 import s3client
from lorgs.models.game_version import GameVersion
from lorgs.models.warcraftlogs_ranking import SpecRanking


def human_readable_size(size: int) -> str:
    if size < 1024:  # ruff: ignore[magic-value-comparison]
        return f"{size}B"
    if size < 1024 * 1024:
        return f"{size / 1024:.2f}KB"
    if size < 1024 * 1024 * 1024:
        return f"{size / 1024 / 1024:.2f}MB"
    return f"{size / 1024 / 1024 / 1024:.2f}GB"


def main(game_version: GameVersion) -> None:
    prefix = f"{game_version.name}/{SpecRanking.get_table_name()}/{game_version.data.season.slug}/"

    start = time.perf_counter()
    requests = 0
    objects = []
    for page in s3client.get_paginator("list_objects_v2").paginate(Bucket=SpecRanking.bucket, Prefix=prefix):
        requests += 1
        objects.extend(page.get("Contents", []))
    duration = time.perf_counter() - start

    objects.sort(key=lambda obj: obj["LastModified"])
    for obj in objects:
        last_modified = obj["LastModified"].isoformat(timespec="seconds")

        size = obj["Size"]
        size_str = human_readable_size(size)
        name = obj["Key"].removeprefix(prefix)
        print(f"{last_modified} | {size_str:>10} | {name}")

    print(f"\n{len(objects)} rankings under s3://{SpecRanking.bucket}/{prefix}")
    print(f"{requests} ListObjectsV2 requests in {duration:.2f}s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--game-version",
        choices=sorted(GAME_VERSIONS),
        help="default: every Game Version with updates enabled",
    )
    args = parser.parse_args()

    if args.game_version:
        game_versions = [GAME_VERSIONS[args.game_version]]
    else:
        game_versions = [gv for gv in GAME_VERSIONS.values() if gv.updates_enabled]
    for game_version in game_versions:
        main(game_version)
