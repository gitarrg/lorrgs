#!/usr/bin/env -S PYTHONPATH=. uv run

# IMPORT STANDARD LIBRARIES
import argparse
import datetime
import itertools

# IMPORT LOCAL LIBRARIES
from lorgs.data import GAME_VERSIONS
from lorgs.models.warcraftlogs_ranking import SpecRanking
from lorrgs_sqs.helpers import all_bosses, all_specs


def main(game_version_name: str) -> None:
    game_version = GAME_VERSIONS[game_version_name]
    game_data = game_version.data
    bosses = all_bosses(game_data)  # the current Season's bosses
    specs = all_specs(game_data)
    metrics = ["dps", "hps"]
    combos = [(spec, boss, difficulty, metric)
              for spec, boss, metric in itertools.product(specs, bosses, metrics)
              for difficulty in game_data.difficulties_for_boss(boss.full_name_slug)]

    for [spec, boss, difficulty, metric] in combos:
        print(spec.full_name_slug, boss.full_name_slug, difficulty, metric)

        spec_ranking = SpecRanking.get_or_create(
            game_version=game_version.name,
            spec_slug=spec.full_name_slug,
            boss_slug=boss.full_name_slug,
            difficulty=difficulty,
            metric=metric,
        )
        if spec_ranking:
            spec_ranking.dirty = True
            spec_ranking.updated = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=4)
            spec_ranking.save()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flag all Spec Rankings of a Game Version as dirty.")
    parser.add_argument("--game-version", default="retail", choices=list(GAME_VERSIONS), help="default: %(default)s")
    main(parser.parse_args().game_version)
    # load_comp_ranking()
