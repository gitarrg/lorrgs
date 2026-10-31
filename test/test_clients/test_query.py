"""Query results parse in the one shape `WarcraftlogsClient.query` returns."""

import pydantic
import pytest

from lorgs.clients import wcl
from lorgs.clients.wcl.models.query import MissingQueryResultError
from test.helpers import load_fixture


def test_report_query_parses() -> None:
    query = wcl.Query.model_validate({"reportData": {"report": {"title": "Raid", "events": {"data": []}}}})
    assert query.report.title == "Raid"


def test_world_query_parses() -> None:
    query = wcl.Query.model_validate(load_fixture("spec_rankings_1.json"))
    assert len(query.world_data.encounter.characterRankings.rankings) > 0


def test_summary_is_unwrapped_from_its_table_data() -> None:
    query = wcl.Query.model_validate(load_fixture("fight_summary_1.json"))
    assert query.report.summary is not None
    assert query.report.summary.totalTime == 728598


def test_an_unwrapped_report_is_rejected() -> None:
    query = wcl.Query.model_validate({"report": {"title": "Raid"}})
    with pytest.raises(MissingQueryResultError, match="reportData"):
        _ = query.report


def test_a_missing_world_data_is_rejected() -> None:
    query = wcl.Query.model_validate({"reportData": {"report": {}}})
    with pytest.raises(MissingQueryResultError, match="worldData"):
        _ = query.world_data


@pytest.mark.parametrize("field", ["events", "summary"])
def test_paginated_fields_need_their_data_wrapper(field: str) -> None:
    with pytest.raises(pydantic.ValidationError, match="Missing `data`"):
        wcl.Query.model_validate({"reportData": {"report": {field: {"totalTime": 1}}}})
