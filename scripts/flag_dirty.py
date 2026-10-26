#!/usr/bin/env -S PYTHONPATH=. uv run

# IMPORT STANDARD LIBRARIES
import datetime
import itertools

# IMPORT LOCAL LIBRARIES
from lorgs.game_version import ACTIVE
from lorgs.models.warcraftlogs_ranking import SpecRanking
from lorrgs_sqs.helpers import ALL_BOSSES, ALL_SPECS


def main() -> None:
    bosses = ALL_BOSSES  # the current Season's bosses
    specs = ALL_SPECS
    metrics = ["dps", "hps"]
    difficulties = ACTIVE.difficulty_names

    for [spec, boss, difficulty, metric] in itertools.product(specs, bosses, difficulties, metrics):
        print(spec.full_name_slug, boss.full_name_slug, difficulty, metric)

        spec_ranking = SpecRanking.get_or_create(
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
    main()
    # load_comp_ranking()
