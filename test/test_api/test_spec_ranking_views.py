"""Every served Spec Ranking logs one view line, counted with CloudWatch Logs Insights (#130)."""

from __future__ import annotations

from test.helpers import get_api_routes

from lorrgs_api.routes import api_spec_rankings


def test_a_served_ranking_logs_a_view_with_its_metric(monkeypatch, caplog) -> None:
    monkeypatch.setattr(api_spec_rankings.warcraftlogs_ranking.SpecRanking, "get_raw", lambda **kwargs: "{}")

    with caplog.at_level("INFO", logger="Lorgs"):
        get_api_routes("/api/retail/spec_ranking/mage-fire/some-boss")

    views = [r.getMessage() for r in caplog.records if r.getMessage().startswith("spec_ranking_view")]
    assert views == [
        "spec_ranking_view game_version=retail spec=mage-fire boss=some-boss "
        "difficulty=auto metric=dps metric_given=False"
    ]


def test_a_missing_ranking_logs_no_view(monkeypatch, caplog) -> None:
    def get_raw(**kwargs):
        raise KeyError

    monkeypatch.setattr(api_spec_rankings.warcraftlogs_ranking.SpecRanking, "get_raw", get_raw)

    with caplog.at_level("INFO", logger="Lorgs"):
        get_api_routes("/api/retail/spec_ranking/mage-fire/some-boss")

    assert not [r for r in caplog.records if r.getMessage().startswith("spec_ranking_view")]
