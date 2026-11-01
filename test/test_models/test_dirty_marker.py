"""Dirty markers: key mapping, save, clear and listing (S3 is mocked)."""

import datetime
from unittest import mock

from lorgs.data import RETAIL
from lorgs.models import dirty_marker
from lorgs.models.dirty_marker import DirtyMarker
from lorgs.models.warcraftlogs_ranking import SpecRanking


SEASON = RETAIL.data.season.slug
FIELDS = {
    "game_version": "retail",
    "spec_slug": "mage-fire",
    "boss_slug": "the-stone-guard",
    "difficulty": "heroic",
    "metric": "dps",
}
RANKING_KEY = f"retail/spec_ranking/{SEASON}/mage-fire/the-stone-guard__heroic__dps"
MARKER_KEY = f"retail/dirty_marker/{SEASON}/mage-fire/the-stone-guard__heroic__dps"


def test_marker_key_mirrors_the_ranking_key() -> None:
    assert SpecRanking.get_key(**FIELDS) == RANKING_KEY
    assert DirtyMarker.get_key(**FIELDS) == MARKER_KEY


def test_a_ranking_knows_its_marker() -> None:
    ranking = SpecRanking(**FIELDS)

    assert ranking.dirty_marker == DirtyMarker(**FIELDS)


def test_save_and_clear_use_the_marker_key() -> None:
    marker = DirtyMarker(**FIELDS)
    with (
        mock.patch("lorgs.models.base.s3.s3client") as saver,
        mock.patch.object(dirty_marker, "s3client") as deleter,
    ):
        marker.save()
        marker.clear()

    assert saver.put_object.call_args.kwargs["Key"] == MARKER_KEY
    deleter.delete_object.assert_called_once_with(Bucket=DirtyMarker.bucket, Key=MARKER_KEY)


def test_list_flagged_maps_markers_back_to_ranking_keys() -> None:
    flagged_at = datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC)
    with mock.patch.object(dirty_marker, "s3client") as s3:
        paginator = s3.get_paginator.return_value
        paginator.paginate.return_value = [{"Contents": [{"Key": MARKER_KEY, "LastModified": flagged_at}]}, {}]

        result = DirtyMarker.list_flagged(RETAIL)

    assert result == {RANKING_KEY: flagged_at}
    assert paginator.paginate.call_args.kwargs["Prefix"] == f"retail/dirty_marker/{SEASON}/"
