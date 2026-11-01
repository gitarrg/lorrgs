#!/usr/bin/env -S PYTHONPATH=. uv run

# IMPORT STANDARD LIBRARIES
import argparse

# IMPORT LOCAL LIBRARIES
from lorgs.data import GAME_VERSIONS
from lorgs.models import dirty_markers, selectors
from lorgs.models.warcraftlogs_ranking import SpecRanking


def main(game_version_name: str) -> None:
    game_version = GAME_VERSIONS[game_version_name]
    game_data = game_version.data
    keys = selectors.expand_selectors(
        game_data,
        selectors.select_specs(game_data, selectors.ALL),
        selectors.select_bosses(game_data, selectors.ALL),  # the current Season's bosses
        difficulty=selectors.ALL,
        metric=selectors.ALL,
    )

    for key in keys:
        print(key.spec.full_name_slug, key.boss.full_name_slug, key.difficulty, key.metric)

        dirty_markers.flag(
            SpecRanking.get_key(
                game_version=game_version.name,
                spec_slug=key.spec.full_name_slug,
                boss_slug=key.boss.full_name_slug,
                difficulty=key.difficulty,
                metric=key.metric,
            ),
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flag all Spec Rankings of a Game Version as dirty.")
    parser.add_argument("--game-version", default="retail", choices=list(GAME_VERSIONS), help="default: %(default)s")
    main(parser.parse_args().game_version)
    # load_comp_ranking()
