"""A Spec Ranking Refresh skips when Warcraft Logs points run low."""

import asyncio
from unittest import mock

import pytest

from lorgs.data import RETAIL
from lorgs.models.task_payloads import SpecRankingPayload
from lorrgs_sqs.task_handlers import load_spec_rankings


def _run(rate_info: dict[str, int]) -> tuple[tuple[bool, str], mock.MagicMock]:
    payload = SpecRankingPayload(
        game_version="retail", spec_slug="priest-holy", boss_slug=RETAIL.data.bosses[0].full_name_slug
    )
    client = mock.Mock(get_rate_info=mock.AsyncMock(return_value=rate_info))
    with (
        mock.patch.object(load_spec_rankings.warcraftlogs_ranking.SpecRanking, "get_or_create") as get_or_create,
        mock.patch.object(load_spec_rankings.WarcraftlogsClient, "get_instance", return_value=client),
        mock.patch.object(load_spec_rankings, "SpecRankingLoader") as loader,
    ):
        get_or_create.return_value.needs_refresh.return_value = True
        loader.return_value.load = mock.AsyncMock()
        result = asyncio.run(load_spec_rankings.load_spec_rankings(payload))
    return result, loader


def test_low_points_skip_the_refresh() -> None:
    result, loader = _run({"limitPerHour": 1000, "pointsSpentThisHour": 900})

    assert result == (True, "skipped: low on points")
    loader.assert_not_called()


@pytest.mark.parametrize(
    "rate_info",
    [
        {"limitPerHour": 1000, "pointsSpentThisHour": 100},
        {},  # Warcraft Logs did not say: don't block
    ],
)
def test_enough_points_refresh(rate_info: dict[str, int]) -> None:
    result, loader = _run(rate_info)

    assert result == (True, "done")
    loader.return_value.load.assert_awaited_once()
