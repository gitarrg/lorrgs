#!/usr/bin/env python
"""Util to fill in some missing data."""
import typing

# from lorgs import data
from lorgs import db
from lorgs import data
from lorgs.models import warcraftlogs_ranking

########################################
#
#
def load_spec_rankings(limit=None):
    print("load_spec_rankings START")

    rankings: typing.List[warcraftlogs_ranking.SpecRanking] = warcraftlogs_ranking.SpecRanking.objects(metric=None)
    if limit:
        rankings = rankings[:limit]

    for ranking in rankings:
        ranking.difficulty = ranking.difficulty or "mythic"
        print("ranking", ranking.spec_slug, ranking.boss_slug, ranking.difficulty, ranking.spec.role.metric)

        ranking.metric = ranking.spec.role.metric
        ranking.save()
    print("load_spec_rankings DONE")


if __name__ == '__main__':
    load_spec_rankings()
