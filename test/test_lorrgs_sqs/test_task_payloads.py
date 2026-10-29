"""Seams: SQS tasks carry their Game Version, and every expanded message keeps it."""

from __future__ import annotations

import asyncio
import json
from unittest import mock

import pydantic
import pytest

from lorgs.clients import sqs
from lorgs.data import MISTS, RETAIL
from lorgs.models.raid_zone import AUTO_DIFFICULTY
from lorgs.models.task_payloads import CompRankingPayload, SpecRankingPayload, UserReportPayload
from lorgs.models.warcraftlogs_ranking import SpecRanking
from lorrgs_sqs import handler, helpers
from lorrgs_sqs.exceptions import TaskValidationError
from lorrgs_sqs.task_handlers import load_spec_rankings


SPEC_PAYLOAD = {"boss_slug": "the-stone-guard", "spec_slug": "mage-fire"}


@pytest.mark.parametrize("payload_cls", [SpecRankingPayload, CompRankingPayload])
def test_a_payload_without_game_version_fails_validation(payload_cls: type[pydantic.BaseModel]) -> None:
    with pytest.raises(pydantic.ValidationError, match="game_version"):
        payload_cls(boss_slug="b", spec_slug="s")


def test_a_user_report_payload_without_game_version_fails_validation() -> None:
    with pytest.raises(pydantic.ValidationError, match="game_version"):
        UserReportPayload(report_id="abc", fight_ids=[1], player_ids=[2])


def test_a_payload_with_an_unknown_game_version_fails_validation() -> None:
    with pytest.raises(pydantic.ValidationError, match="Unknown Game Version"):
        SpecRankingPayload(game_version="classic", **SPEC_PAYLOAD)


def test_the_difficulty_defaults_to_auto() -> None:
    assert SpecRankingPayload(game_version="mists", **SPEC_PAYLOAD).difficulty == AUTO_DIFFICULTY


def test_the_payload_resolves_its_game_version() -> None:
    assert SpecRankingPayload(game_version="mists", **SPEC_PAYLOAD).get_game_version() is MISTS


################################################################################
# Keyword expansion
#


def test_expansion_uses_the_game_data_of_the_payloads_game_version() -> None:
    mists = helpers.expand_keywords({"game_version": "mists", "boss_slug": "all", "spec_slug": "mage-fire"})
    retail = helpers.expand_keywords({"game_version": "retail", "boss_slug": "all", "spec_slug": "mage-fire"})

    assert {p["boss_slug"] for p in mists} == {boss.full_name_slug for boss in MISTS.data.bosses}
    assert {p["boss_slug"] for p in retail} == {boss.full_name_slug for boss in RETAIL.data.bosses}


def test_expanded_payloads_keep_the_game_version() -> None:
    payloads = helpers.expand_keywords({"game_version": "mists", "boss_slug": "all", "spec_slug": "all"})

    assert len(payloads) > 1
    assert {payload["game_version"] for payload in payloads} == {"mists"}


def test_expansion_without_a_valid_game_version_is_a_validation_error() -> None:
    with pytest.raises(TaskValidationError):
        helpers.expand_keywords({"boss_slug": "all"})
    with pytest.raises(TaskValidationError):
        helpers.expand_keywords({"game_version": "classic", "boss_slug": "all"})


def test_expanded_messages_are_in_a_message_group_of_their_game_version() -> None:
    body = json.dumps({"task": "load_spec_rankings", "game_version": "mists", "boss_slug": "all", **{"spec_slug": "mage-fire"}})
    message = {"body": body, "eventSourceARN": "arn:aws:sqs:eu-west-1:1:queue.fifo"}

    with mock.patch.object(handler, "submit_messages") as submit_messages:
        asyncio.run(handler.process_message(message))

    messages = submit_messages.call_args.args[1]
    assert len(messages) > 1
    assert all(json.loads(m["MessageBody"])["game_version"] == "mists" for m in messages)
    assert all(m["MessageGroupId"].startswith("mists-") for m in messages)
    assert len({m["MessageGroupId"] for m in messages}) == len(messages)


def test_message_groups_of_different_game_versions_differ() -> None:
    assert sqs.new_message_group({"game_version": "mists"}).startswith("mists-")
    assert sqs.new_message_group(SpecRankingPayload(game_version="retail", **SPEC_PAYLOAD)).startswith("retail-")


def test_sending_a_message_uses_the_game_version_as_message_group() -> None:
    payload = SpecRankingPayload(game_version="mists", **SPEC_PAYLOAD)
    with mock.patch.object(sqs, "SQS_CLIENT") as client:
        sqs.send_message(payload)
    assert client.send_message.call_args.kwargs["MessageGroupId"].startswith("mists-")


################################################################################
# Handlers
#


def test_spec_ranking_handler_loads_into_the_requested_game_versions_ranking() -> None:
    payload = SpecRankingPayload(game_version="mists", metric="dps", **SPEC_PAYLOAD)
    saved: list[SpecRanking] = []

    async def fake_load(self, *args, **kwargs):  # noqa: ANN001, ANN002, ANN003
        assert self.ranking.game_version == "mists"
        assert self.game_data is MISTS.data

    with (
        mock.patch.object(SpecRanking, "get", classmethod(lambda cls, **kwargs: None)),
        mock.patch.object(SpecRanking, "save", lambda self: saved.append(self)),
        mock.patch.object(load_spec_rankings.SpecRankingLoader, "load", fake_load),
    ):
        assert asyncio.run(load_spec_rankings.load_spec_rankings(payload)) == (True, "done")

    (ranking,) = saved
    assert ranking.game_version == "mists"
    assert ranking.difficulty == "heroic"  # `auto` resolved for the boss
    assert SpecRanking.get_key(**dict(ranking)).startswith("mists/spec_ranking/")


def test_spec_ranking_handler_rejects_a_boss_of_another_game_version() -> None:
    payload = SpecRankingPayload(game_version="retail", **SPEC_PAYLOAD)  # a Mists boss
    with pytest.raises(TaskValidationError, match="invalid boss"):
        asyncio.run(load_spec_rankings.load_spec_rankings(payload))
