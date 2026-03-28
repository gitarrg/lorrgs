#!/usr/bin/env python
"""Util to fill in some missing data."""

import asyncio
import os

import arrow
import mongoengine as me
from lorgs.lib import mongoengine_arrow

from lorgs import data
from lorgs import db
# from lorgs.models import warcraftlogs_ranking

########################################
#
#
class OldFight(me.EmbeddedDocument):
    start_time: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField()
    end_time: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField()

    duration = me.IntField(default=0)

    meta = {
        "strict": False # ignore non existing properties
    }

class OldReport(me.EmbeddedDocument):

    report_id = me.StringField(primary_key=True)
    start_time: arrow.Arrow = mongoengine_arrow.ArrowDateTimeField()
    fights = me.ListField(me.EmbeddedDocumentField(OldFight))

    meta = {
        "strict": False # ignore non existing properties
    }


class OldSpecRanking(me.Document):

    reports = me.ListField(me.EmbeddedDocumentField(OldReport))

    boss_slug = me.StringField()
    spec_slug = me.StringField()

    meta = {
        "collection": "spec_ranking",   # <-- read the actual reports
        "strict": False # ignore non existing properties
    }


def fix_fight_duration(report, fight):
    fight.start_time = report.start_time.shift(seconds=fight.start_time.timestamp/1000)
    end_time = report.start_time.shift(seconds=fight.end_time.timestamp/1000)

    # d = end_time - fight.start_time
    fight.duration = (end_time.timestamp - fight.start_time.timestamp) * 1000

    print("\tF: s", fight.start_time, "-", end_time, fight.duration)


def fix_duration(boss=None, spec=None):
    """Find all Spec Rankings without duration attribute."""

    old_rankings = OldSpecRanking.objects()
    if boss:
        old_rankings = old_rankings.filter(boss_slug=boss.full_name_slug)
    if spec:
        old_rankings = old_rankings.filter(spec_slug=spec.full_name_slug)
    old_rankings = old_rankings.filter(reports__fights__duration__not__exists=1)
    old_rankings = old_rankings.all()

    for ranking in old_rankings:
        print("R", ranking, ranking.boss_slug, ranking.spec_slug)
        for report in ranking.reports:
            print("\t", report, report.report_id)
            for fight in report.fights:
                fix_fight_duration(report, fight)
        ranking.save()


def main():
    fix_duration()
    print("done")


if __name__ == '__main__':
    main()
