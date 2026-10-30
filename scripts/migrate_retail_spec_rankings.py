#!/usr/bin/env -S PYTHONPATH=. uv run
"""Copy the un-prefixed Retail Spec Rankings into `retail/spec_ranking/`.

`spec_ranking/{spec}/{file}` goes to `retail/spec_ranking/{season}/{spec}/{file}`
when spec and boss belong to Retail's current season, else to
`retail/spec_ranking/old/{spec}/{file}`. Adds the now required `game_version`.
Source files are left in place. Dry run unless `--execute`.
"""

# IMPORT STANDARD LIBRARIES
import argparse
import json
from concurrent.futures import ThreadPoolExecutor

# IMPORT LOCAL LIBRARIES
from lorgs.data import RETAIL
from lorgs.models.base.s3 import s3client
from lorgs.models.warcraftlogs_ranking import SpecRanking


SRC_PREFIX = "spec_ranking/"
DST_PREFIX = f"{RETAIL.name}/spec_ranking/"


def list_keys(bucket: str, prefix: str) -> list[str]:
    paginator = s3client.get_paginator("list_objects_v2")
    return [obj["Key"] for page in paginator.paginate(Bucket=bucket, Prefix=prefix) for obj in page.get("Contents", [])]


def get_destination(src_key: str) -> str:
    game_data = RETAIL.data
    spec_slug, filename = src_key.removeprefix(SRC_PREFIX).split("/", 1)
    boss_slug = filename.split("__")[0]

    fits = spec_slug in game_data.specs_by_slug and boss_slug in game_data.bosses_by_slug
    folder = game_data.season.slug if fits else "old"
    return f"{DST_PREFIX}{folder}/{spec_slug}/{filename}"


def copy(bucket: str, src_key: str, dst_key: str) -> None:
    body = s3client.get_object(Bucket=bucket, Key=src_key)["Body"].read()
    data = {"game_version": RETAIL.name, **json.loads(body)}
    s3client.put_object(
        Bucket=bucket,
        Key=dst_key,
        Body=json.dumps(data, separators=(",", ":")),
        ContentType="application/json",
    )
    print(f"{src_key} -> {dst_key}")


def main(*, execute: bool, overwrite: bool) -> None:
    bucket = SpecRanking.bucket
    existing = set(list_keys(bucket, DST_PREFIX))

    jobs: list[tuple[str, str]] = []
    skipped = 0
    for src_key in list_keys(bucket, SRC_PREFIX):
        dst_key = get_destination(src_key)
        if dst_key in existing and not overwrite:
            skipped += 1
            continue
        jobs.append((src_key, dst_key))

    season_prefix = f"{DST_PREFIX}{RETAIL.data.season.slug}/"
    to_season = sum(dst.startswith(season_prefix) for _, dst in jobs)
    print(f"{to_season} -> {season_prefix}")
    print(f"{len(jobs) - to_season} -> {DST_PREFIX}old/")
    print(f"{skipped} skipped (already in {DST_PREFIX}; --overwrite to replace)")

    if not execute:
        for src_key, dst_key in jobs[:10]:
            print(f"  {src_key} -> {dst_key}")
        print("dry run: pass --execute to copy")
        return

    with ThreadPoolExecutor(max_workers=32) as pool:
        for future in [pool.submit(copy, bucket, src, dst) for src, dst in jobs]:
            future.result()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--execute", action="store_true", help="copy (default: dry run)")
    parser.add_argument("--overwrite", action="store_true", help="replace rankings already in the destination")
    args = parser.parse_args()
    main(execute=args.execute, overwrite=args.overwrite)
