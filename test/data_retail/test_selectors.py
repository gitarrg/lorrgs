"""Retail: selecting `all` specs never picks the item pseudo-specs, and a payload's metric defaults to the spec's role."""

import typing

import asyncio
from unittest import mock

from lorgs.data import RETAIL
from lorgs.models import selectors
from lorgs.models.task_payloads import SpecRankingPayload
from lorrgs_sqs import helpers
from lorrgs_sqs.task_handlers import load_spec_rankings


def test_all_specs_are_playable() -> None:
    slugs = {spec.full_name_slug for spec in selectors.select_specs(RETAIL.data, "all")}

    assert "mage-fire" in slugs
    assert not any(slug.startswith("other-") for slug in slugs)


def test_scheduled_payload_skips_pseudo_specs() -> None:
    payloads = helpers.expand_keyword("spec_slug", [{"game_version": "retail", "spec_slug": "all"}])

    assert payloads
    assert not any(payload["spec_slug"].startswith("other-") for payload in payloads)


def test_racials_are_a_pseudo_spec_every_player_queries() -> None:
    racials = RETAIL.data.get_spec("other-racials")
    berserking = RETAIL.data.get_spell(26297)
    assert berserking is not None
    assert racials and not racials.role.playable
    assert berserking.spell_type == "other-racials"
    assert all(berserking in spec.spells for spec in selectors.playable_specs(RETAIL.data))


def test_payload_metric_defaults_to_the_role() -> None:
    payload = SpecRankingPayload(
        game_version="retail", spec_slug="priest-holy", boss_slug=RETAIL.data.bosses[0].full_name_slug
    )

    with mock.patch.object(load_spec_rankings.warcraftlogs_ranking.SpecRanking, "get_or_create") as get_or_create:
        get_or_create.return_value.needs_refresh.return_value = False
        asyncio.run(load_spec_rankings.load_spec_rankings(payload))

    assert get_or_create.call_args.kwargs["metric"] == "hps"
