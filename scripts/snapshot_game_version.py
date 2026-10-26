#!/usr/bin/env -S PYTHONPATH=. uv run
"""Snapshot what the backend serves and stores, to diff behaviour across refactors.

Dumps, as JSON:
    - the responses of the static-data API routes (world data, specs, spells, season)
    - the S3 keys / DynamoDB keys computed for a set of sample inputs

Needs no network, AWS or Redis access: route handlers are called directly and keys
are only computed, never read or written.

The snapshot is a review aid, not a golden test: run it before and after a change
(with `LORRGS_GAME_VERSION` unset to snapshot Retail) and diff the two files.

Usage:
    scripts/snapshot_game_version.py /tmp/before.json
    # ... change code ...
    scripts/snapshot_game_version.py /tmp/after.json
    diff /tmp/before.json /tmp/after.json && echo "no change"

The output is key-sorted and indented, so a plain `diff` is line-oriented.
"""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import argparse
import asyncio
import json
import pathlib
import typing

# IMPORT THIRD PARTY LIBRARIES
from fastapi.encoders import jsonable_encoder

# IMPORT LOCAL LIBRARIES
from lorgs import data  # ruff: ignore[unused-import]  # registers the game data
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.raid_zone import RaidZone
from lorgs.models.season import Season
from lorgs.models.user import User
from lorgs.models.warcraftlogs_comp_ranking import CompRanking
from lorgs.models.warcraftlogs_ranking import SpecRanking
from lorgs.models.warcraftlogs_user_report import UserReport
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import WowSpell
from lorgs.models.wow_trinket import WowTrinket
from lorrgs_api.routes import api_season, api_world_data


# sample inputs for keys that are not derived from the game data
DIFFICULTIES = ["heroic", "mythic", "normal"]
REPORT_IDS = ["aBcD1234eFgH5678"]
DISCORD_IDS = ["123456789012345678"]


def call(handler: typing.Callable[..., typing.Any], *args: typing.Any) -> typing.Any:
    """Call a route handler directly and encode the result like FastAPI would."""
    return jsonable_encoder(asyncio.run(handler(*args)))


def dump(obj: typing.Any) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False)


def sorted_list(items: list[typing.Any]) -> list[typing.Any]:
    """Sort by content.

    `MemoryModel.list()` returns instances in arbitrary order (it is backed by a `WeakSet`),
    so routes built on it are not stable between runs. Their order is not part of what we diff.
    """
    return sorted(items, key=dump)


def variants(models: typing.Iterable[typing.Any]) -> dict[str, typing.Any]:
    """Every distinct payload per `spell_id`, for routes that key a response by `spell_id`.

    Several spells/trinkets share one `spell_id`, and the routes keep an arbitrary one of them
    (whichever `WeakSet` iteration yields last). We list them all instead.
    """
    grouped: dict[int, set[str]] = {}
    for model in models:
        grouped.setdefault(model.spell_id, set()).add(dump(jsonable_encoder(model)))
    return {str(spell_id): sorted(payloads) for spell_id, payloads in sorted(grouped.items())}


################################################################################
# API responses
#


def snapshot_world_data() -> dict[str, typing.Any]:
    routes: dict[str, typing.Any] = {}

    routes["/roles"] = {"roles": sorted_list(call(api_world_data.get_roles)["roles"])}
    routes["/specs"] = call(api_world_data.get_specs_all)
    routes["/zones"] = sorted_list(call(api_world_data.get_zones))
    routes["/bosses"] = {"bosses": sorted_list(call(api_world_data.get_bosses)["bosses"])}

    classes = call(api_world_data.get_classes)
    for class_data in classes.values():
        class_data["spec_ids"] = sorted(class_data["spec_ids"])
    routes["/classes"] = classes

    # the id set the route answers with, and every payload it could answer with for each id
    routes["/spells"] = {
        "ids": sorted(call(api_world_data.spells_all)),
        "variants": variants(WowSpell.list()),
    }
    routes["/trinkets"] = {
        "ids": sorted(call(api_world_data.trinkets_all)),
        "variants": variants(WowTrinket.list()),
    }

    for spec in sorted(WowSpec.list()):
        routes[f"/specs/{spec.full_name_slug}"] = call(api_world_data.get_spec, spec.full_name_slug)
        routes[f"/specs/{spec.full_name_slug}/spells"] = call(api_world_data.get_spec_spells, spec.full_name_slug)

    for zone in sorted(RaidZone.list(), key=lambda z: z.id):
        routes[f"/zones/{zone.id}"] = call(api_world_data.get_zone, zone.id)
        routes[f"/zones/{zone.id}/bosses"] = call(api_world_data.get_zone_bosses, zone.id)

    for boss in sorted(RaidBoss.list(), key=lambda b: b.full_name_slug):
        routes[f"/bosses/{boss.full_name_slug}"] = call(api_world_data.get_boss, boss.full_name_slug)
        routes[f"/bosses/{boss.full_name_slug}/spells"] = call(api_world_data.get_boss_spells, boss.full_name_slug)

    return routes


def snapshot_season() -> dict[str, typing.Any]:
    routes: dict[str, typing.Any] = {"/seasons/current": call(api_season.get_season, "current")}
    for season in sorted(Season.list(), key=lambda s: s.slug):
        routes[f"/seasons/{season.slug}"] = call(api_season.get_season, season.slug)
    return routes


################################################################################
# Storage keys
#


def snapshot_keys() -> dict[str, typing.Any]:
    specs = sorted(WowSpec.list())
    bosses = sorted(RaidBoss.list(), key=lambda b: b.full_name_slug)

    spec_rankings = [
        SpecRanking.get_key(
            spec_slug=spec.full_name_slug,
            boss_slug=boss.full_name_slug,
            difficulty=difficulty,
            metric=spec.role.metric,
        )
        for spec in specs
        for boss in bosses
        for difficulty in DIFFICULTIES
    ]
    comp_rankings = [CompRanking.get_key(boss_slug=boss.full_name_slug) for boss in bosses]

    return {
        "s3": {
            "bucket": SpecRanking.bucket,
            "spec_ranking": spec_rankings,
            "comp_ranking": comp_rankings,
        },
        "dynamodb": {
            "user_report": {
                "table": UserReport.get_table_name(),
                "keys": [UserReport.get_keys(report_id=report_id) for report_id in REPORT_IDS],
            },
            "user": {
                "table": User.get_table_name(),
                "keys": [User.get_keys(discord_id=discord_id) for discord_id in DISCORD_IDS],
            },
        },
    }


################################################################################
# main
#


def build_snapshot() -> dict[str, typing.Any]:
    return {
        "api": {**snapshot_world_data(), **snapshot_season()},
        "keys": snapshot_keys(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("output", type=pathlib.Path, help="Path to write the snapshot JSON to.")
    args = parser.parse_args()

    snapshot = build_snapshot()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(snapshot, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
