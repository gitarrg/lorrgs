"""Off-metric Spec Rankings get a refresh interval, default metrics do not."""

from __future__ import annotations

import datetime

from lorgs.data import RETAIL
from lorgs.models import ranking_status, refresh_planner
from lorgs.models.task_payloads import SpecRankingPayload


def test_only_off_metrics_get_a_refresh_interval(monkeypatch) -> None:
    healer = next(spec for spec in RETAIL.data.specs if spec.role.code == "heal")
    payloads = {
        f"retail/{metric}": SpecRankingPayload(
            game_version="retail", spec_slug=healer.full_name_slug, boss_slug="boss", difficulty="heroic", metric=metric
        )
        for metric in ("hps", "dps")
    }
    monkeypatch.setattr(ranking_status, "list_last_modified", lambda gv: {})
    monkeypatch.setattr(ranking_status.DirtyMarker, "list_flagged", lambda gv: {})

    by_key = {c.key: c for c in ranking_status.get_candidates(RETAIL, payloads)}

    assert by_key["retail/hps"].refresh_interval == datetime.timedelta(0)
    assert by_key["retail/dps"].refresh_interval == refresh_planner.OFF_METRIC_REFRESH_INTERVAL
