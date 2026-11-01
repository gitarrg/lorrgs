"""Dirty markers: key mapping and listing (S3 is mocked)."""

import datetime
from unittest import mock

from lorgs.data import RETAIL
from lorgs.models import dirty_markers
from lorgs.models.warcraftlogs_ranking import SpecRanking


RANKING_KEY = "retail/spec_ranking/midnight_s2/mage-fire/the-stone-guard__heroic__dps"
MARKER_KEY = "retail/spec_ranking_dirty/midnight_s2/mage-fire/the-stone-guard__heroic__dps"


def test_marker_key_mirrors_the_ranking_key() -> None:
    assert dirty_markers.marker_key(RANKING_KEY) == MARKER_KEY
    assert dirty_markers.ranking_key(MARKER_KEY) == RANKING_KEY


def test_flag_and_clear_write_the_marker() -> None:
    with mock.patch.object(dirty_markers, "s3client") as s3:
        dirty_markers.flag(RANKING_KEY)
        dirty_markers.clear(RANKING_KEY)

    s3.put_object.assert_called_once_with(Bucket=SpecRanking.bucket, Key=MARKER_KEY, Body=b"")
    s3.delete_object.assert_called_once_with(Bucket=SpecRanking.bucket, Key=MARKER_KEY)


def test_list_flagged_maps_markers_back_to_ranking_keys() -> None:
    flagged_at = datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC)
    with mock.patch.object(dirty_markers, "s3client") as s3:
        paginator = s3.get_paginator.return_value
        paginator.paginate.return_value = [{"Contents": [{"Key": MARKER_KEY, "LastModified": flagged_at}]}, {}]

        result = dirty_markers.list_flagged(RETAIL)

    assert result == {RANKING_KEY: flagged_at}
    assert paginator.paginate.call_args.kwargs["Prefix"] == f"retail/spec_ranking_dirty/{RETAIL.data.season.slug}/"
