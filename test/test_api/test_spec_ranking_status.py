"""`/spec_ranking/status` reports the rankings the way the Refresh Planner sees them."""

from __future__ import annotations

import datetime

from test.helpers import get_api_routes

from lorgs.models.task_payloads import SpecRankingPayload
from lorrgs_api.routes import api_spec_rankings


def test_status_lists_last_refreshed_and_dirty_since(monkeypatch) -> None:
    now = datetime.datetime.now(datetime.UTC)
    payloads = {
        f"retail/{spec}": SpecRankingPayload(
            game_version="retail", spec_slug=spec, boss_slug="boss", difficulty="heroic", metric="dps"
        )
        for spec in ("a", "b")
    }
    monkeypatch.setattr(api_spec_rankings.ranking_status, "get_ranking_payloads", lambda gv: payloads)
    monkeypatch.setattr(api_spec_rankings.ranking_status, "list_last_modified", lambda gv: {"retail/a": now})
    monkeypatch.setattr(api_spec_rankings.ranking_status.DirtyMarker, "list_flagged", lambda gv: {"retail/b": now})

    path = "/api/retail/spec_ranking/status"
    status, body = get_api_routes(path)[path]
    assert status == 200
    by_spec = {row["spec_slug"]: row for row in body}
    assert by_spec["a"]["is_default_metric"]
    assert by_spec["a"]["last_refreshed"] is not None and by_spec["a"]["dirty_since"] is None
    assert by_spec["b"]["last_refreshed"] is None and by_spec["b"]["dirty_since"] is not None
