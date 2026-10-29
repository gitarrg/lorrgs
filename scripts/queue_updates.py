#!/usr/bin/env -S PYTHONPATH=. uv run --env-file=.env
"""Update spec rankings for one or more specs on one or more bosses, raids or a whole Game Version.

Selectors (all repeatable; leaving a group out selects everything in it):
    bosses: --boss or --raid (mutually exclusive). Default: all raids of the current season.
    specs:  --spec, --class, --role (combined as a union). Default: all specs.

Examples (add --dry-run to only print what would be queued):

    # everything: all specs x all bosses of the current season (Retail, remote)
    scripts/queue_updates.py

    # one MoP Classic boss, all specs, top 5 players, run locally
    scripts/queue_updates.py --game-version mists --boss the-stone-guard --limit 5 --mode local

    # all bosses on Retail for a single spec
    scripts/queue_updates.py --spec mage-fire

    # one raid zone, damage dealers only, mythic
    scripts/queue_updates.py --raid the-venomous-abyss --role dps --difficulty mythic

    # two bosses, two specs, both difficulties, wiping old data first
    scripts/queue_updates.py --boss kithix --boss nymrissa-wavecaller --spec mage-fire --spec priest-holy --difficulty all --clear

    # all healers and tanks on one boss, skipping the confirmation prompt
    scripts/queue_updates.py --boss ulatek --role heal --role tank --yes

    # a whole MoP raid for one class, all metrics
    scripts/queue_updates.py --game-version mists --raid throne-of-thunder --class monk --metric all

    # an entire Game Version (every raid of its current season)
    scripts/queue_updates.py --game-version mists --yes

"""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import argparse
import asyncio
import dataclasses
import sys


# IMPORT LOCAL LIBRARIES
from lorgs.clients import sqs
from lorgs.data import GAME_VERSIONS
from lorgs.models.game_data import GameData
from lorgs.models.game_version import GameVersion
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.raid_zone import AUTO_DIFFICULTY, RaidZone
from lorgs.models.task_payloads import SpecRankingPayload
from lorgs.models.wow_spec import WowSpec
from lorrgs_sqs.helpers import all_specs


@dataclasses.dataclass(frozen=True)
class RankingTask:
    """One spec ranking to update."""

    game_version: GameVersion
    spec: WowSpec
    boss: RaidBoss
    difficulty: str
    metric: str


async def load_remote(task: RankingTask, *, limit: int = 50, clear: bool = False):
    payload = SpecRankingPayload(
        game_version=task.game_version.name,
        spec_slug=task.spec.full_name_slug,
        boss_slug=task.boss.full_name_slug,
        difficulty=task.difficulty,
        metric=task.metric,
        limit=limit,
        clear=clear,
    )
    return sqs.send_message(payload=payload)


async def load_local(task: RankingTask, *, limit: int = 50, clear: bool = False):
    # ruff: disable[import-outside-top-level]
    from lorgs.clients.wcl import WarcraftlogsClient
    from lorgs.loaders.spec_ranking import SpecRankingLoader
    from lorgs.models.warcraftlogs_ranking import SpecRanking
    # ruff: enable[import-outside-top-level]

    spec_ranking = SpecRanking.get_or_create(
        game_version=task.game_version.name,
        spec_slug=task.spec.full_name_slug,
        boss_slug=task.boss.full_name_slug,
        difficulty=task.difficulty,
        metric=task.metric,
    )

    client = WarcraftlogsClient.get_instance()
    await SpecRankingLoader(spec_ranking, task.game_version).load(client, limit=limit, clear_old=clear)

    spec_ranking.save()


def load_comp_ranking(game_version: GameVersion, boss_slug: str = "all"):
    payload = {
        "task": "load_comp_rankings",
        "game_version": game_version.name,
        "boss_slug": boss_slug,
    }
    print("q", payload)
    return sqs.send_message(payload=payload)


def load_all(game_version: GameVersion):
    payload = {
        "task": "load_spec_rankings",
        "game_version": game_version.name,
        "spec_slug": "all",
        "boss_slug": "all",
        "difficulty": AUTO_DIFFICULTY,
        "metric": "all",
        "limit": 50,
        "clear": False,
    }
    print("q", payload)
    return sqs.send_message(payload=payload)


################################################################################
# Selection
#


def _season_raids(game_data: GameData) -> list[RaidZone]:
    """The raids of the current season. We never queue older ones."""
    return list(game_data.season.raids)


def _pick(parser: argparse.ArgumentParser, kind: str, wanted: list[str], available: dict) -> list:
    """Look up every slug in `wanted`; fail with the valid choices if one is unknown."""
    unknown = [slug for slug in wanted if slug not in available]
    if unknown:
        parser.error(f"unknown {kind} slug: {', '.join(unknown)}\nvalid {kind} slugs: {', '.join(sorted(available))}")
    return [available[slug] for slug in dict.fromkeys(wanted)]


def select_bosses(parser: argparse.ArgumentParser, args: argparse.Namespace, game_data: GameData) -> list[RaidBoss]:
    if args.raid:
        raids = _pick(parser, "raid", args.raid, {raid.name_slug: raid for raid in _season_raids(game_data)})
        return [boss for raid in raids for boss in raid.bosses]

    if args.boss:
        bosses = {}
        for raid in _season_raids(game_data):
            bosses.update({boss.full_name_slug: boss for boss in raid.bosses})
        return _pick(parser, "boss", args.boss, bosses)

    return [boss for raid in _season_raids(game_data) for boss in raid.bosses]


def select_specs(parser: argparse.ArgumentParser, args: argparse.Namespace, game_data: GameData) -> list[WowSpec]:
    specs_available = all_specs(game_data)
    if not (args.spec or args.wow_class or args.role):
        return sorted(specs_available)

    specs: set[WowSpec] = set()
    specs.update(_pick(parser, "spec", args.spec, {spec.full_name_slug: spec for spec in specs_available}))
    for class_slug in _pick(parser, "class", args.wow_class, {spec.wow_class.name_slug: spec.wow_class.name_slug for spec in specs_available}):
        specs.update(spec for spec in specs_available if spec.wow_class.name_slug == class_slug)
    for role_code in _pick(parser, "role", args.role, {code: code for code in ROLE_CHOICES}):
        codes = {"mdps", "rdps"} if role_code == "dps" else {role_code}
        specs.update(spec for spec in specs_available if spec.role.code in codes)
    return sorted(specs)


def difficulties_for(game_data: GameData, boss: RaidBoss, difficulty: str) -> list[str]:
    """The difficulties to update for a boss. `all` is every difficulty we rank for it, `auto` its zone's one."""
    if difficulty == "all":
        return game_data.difficulties_for_boss(boss.full_name_slug)
    return [game_data.resolve_difficulty(boss.full_name_slug, difficulty)]


def build_tasks(
    game_version: GameVersion,
    specs: list[WowSpec],
    bosses: list[RaidBoss],
    difficulty: str,
    metric: str,
) -> list[RankingTask]:
    tasks = []
    for spec in specs:
        if metric == "all":
            metrics = spec.role.metrics
        else:
            metrics = [metric or spec.role.metric]
        tasks.extend(
            RankingTask(game_version, spec, boss, boss_difficulty, spec_metric)
            for boss in bosses
            for boss_difficulty in difficulties_for(game_version.data, boss, difficulty)
            for spec_metric in metrics
        )
    return tasks


################################################################################
# CLI
#

ROLE_CHOICES = sorted({role.code for version in GAME_VERSIONS.values() for role in version.data.roles}) + ["dps"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--game-version", default="retail", choices=list(GAME_VERSIONS), help="default: %(default)s")
    parser.add_argument("--mode", default="remote", choices=["local", "remote"], help="remote = queue SQS messages (default)")

    bosses = parser.add_argument_group("bosses (default: all raids of the current season)")
    bosses = bosses.add_mutually_exclusive_group()
    bosses.add_argument("--raid", action="append", default=[], metavar="SLUG", help="all bosses of a raid zone, e.g. manaforge-omega")
    bosses.add_argument("--boss", action="append", default=[], metavar="SLUG", help="a single boss, e.g. dimensius")

    specs = parser.add_argument_group("specs (default: all; combined as a union)")
    specs.add_argument("--spec", action="append", default=[], metavar="SLUG", help="e.g. mage-fire")
    specs.add_argument("--class", dest="wow_class", action="append", default=[], metavar="SLUG", help="all specs of a class, e.g. mage")
    specs.add_argument("--role", action="append", default=[], choices=ROLE_CHOICES, help="all specs of a role (dps = mdps + rdps)")

    parser.add_argument(
        "--difficulty",
        default=AUTO_DIFFICULTY,
        choices=[AUTO_DIFFICULTY, *sorted({name for v in GAME_VERSIONS.values() for name in v.difficulty_names}), "all"],
        help="`auto` = the one difficulty ranked per raid, `all` = every difficulty ranked per raid. default: %(default)s",
    )
    parser.add_argument("--metric", default="", help="dps, hps, ... or `all`. default: the spec's role metric")
    parser.add_argument("--limit", type=int, default=50, help="players per ranking. default: %(default)s")
    parser.add_argument("--clear", action=argparse.BooleanOptionalAction, default=False, help="wipe existing data first. default: off")

    parser.add_argument("--dry-run", action="store_true", help="print the summary and exit")
    parser.add_argument("-y", "--yes", action="store_true", help="skip the confirmation prompt")
    return parser


def print_summary(args: argparse.Namespace, game_version: GameVersion, specs: list[WowSpec], bosses: list[RaidBoss], tasks: list[RankingTask]) -> None:
    print(f"game version: {game_version.name}   mode: {args.mode}   limit: {args.limit}   clear: {args.clear}")
    print(f"bosses ({len(bosses)}): {', '.join(boss.full_name_slug for boss in bosses)}")
    print(f"specs ({len(specs)}): {', '.join(spec.full_name_slug for spec in specs)}")
    print(f"difficulties: {', '.join(sorted({task.difficulty for task in tasks}))}   metric: {args.metric or '(role default)'}")
    print(f"=> {len(tasks)} tasks")


def confirm() -> bool:
    try:
        return input("Proceed? [y/N] ").strip().lower() in ("y", "yes")
    except EOFError:
        return False


async def run(tasks: list[RankingTask], args: argparse.Namespace) -> None:
    load = load_local if args.mode == "local" else load_remote
    for i, task in enumerate(tasks, start=1):
        print(f"[{i}/{len(tasks)}] {task.spec.full_name_slug} {task.boss.full_name_slug} {task.difficulty} {task.metric}")
        await load(task, limit=args.limit, clear=args.clear)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    game_version = GAME_VERSIONS[args.game_version]
    bosses = select_bosses(parser, args, game_version.data)
    specs = select_specs(parser, args, game_version.data)
    tasks = build_tasks(game_version, specs, bosses, args.difficulty, args.metric)
    if not tasks:
        parser.error("nothing selected")

    print_summary(args, game_version, specs, bosses, tasks)
    if args.dry_run:
        return
    if not args.yes and not confirm():
        sys.exit("aborted")

    asyncio.run(run(tasks, args))


if __name__ == "__main__":
    main()
