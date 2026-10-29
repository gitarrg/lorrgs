from __future__ import annotations

from collections.abc import Callable
from typing import Any

from lorgs.data import GAME_VERSIONS
from lorgs.models.game_data import GameData
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.wow_spec import WowSpec
from lorrgs_sqs.exceptions import TaskValidationError


def get_game_data(payload: dict) -> GameData:
    """The Game Data of the Game Version the payload belongs to."""
    name = payload.get("game_version")
    if name not in GAME_VERSIONS:
        raise TaskValidationError(f"Invalid game_version: {name!r}")
    return GAME_VERSIONS[name].data


def all_specs(game_data: GameData) -> set[WowSpec]:
    """The class specs of the Game Version (no item pseudo-specs)."""
    return {spec for role in game_data.roles for spec in role.specs}


def all_bosses(game_data: GameData) -> list[RaidBoss]:
    """The bosses of the current season's raids."""
    return [boss for zone in game_data.zones for boss in zone.bosses]


def expand_spec_slug(payload: dict) -> list[str]:
    return [spec.full_name_slug for spec in all_specs(get_game_data(payload))]


def expand_boss_slug(payload: dict) -> list[str]:
    return [boss.full_name_slug for boss in all_bosses(get_game_data(payload))]


def expand_metric(payload: dict) -> list[str]:
    game_data = get_game_data(payload)
    spec = game_data.get_spec(payload.get("spec_slug", ""))
    role = (spec and spec.role) or game_data.get_role("tank")
    return (role and role.metrics) or []


def expand_difficulty(payload: dict) -> list[str]:
    return get_game_data(payload).difficulties_for_boss(payload.get("boss_slug", ""))


PAYLOAD_EXPANDERS: dict[str, Callable[[Any], list[str]]] = {
    "spec_slug": expand_spec_slug,
    "boss_slug": expand_boss_slug,
    "difficulty": expand_difficulty,
    "metric": expand_metric,
}


def expand_payload(keyword: str, payload: dict) -> list[dict]:
    if payload.get(keyword) != "all":
        return [payload]

    values = PAYLOAD_EXPANDERS[keyword](payload)

    return [{**payload, keyword: value} for value in values]


def expand_keyword(keyword, payloads) -> list[dict]:
    """Expand a single Keyword."""
    result = []
    for payload in payloads:
        result += expand_payload(keyword, payload)
    return result


def expand_keywords(payload, cap=10) -> list[dict]:
    """Expand a single Payload replacing `all` Keywords with the actual values."""
    payloads = [payload]

    steps = 0
    for keyword in PAYLOAD_EXPANDERS:
        payloads = expand_keyword(keyword, payloads)

        if len(payloads) > 1:
            steps += 1

        if steps >= cap:
            return payloads

    return payloads


def queue_arn_to_url(arn: str = ""):
    """Converts an SQS Queue ARN into the URL Version.

    >>> queue_arn_to_url("arn:aws:sqs:eu-west-1:12345678:my_queue.fifo")
    https://sqs.eu-west-1.amazonaws.com/12345678/my_queue.fifo

    """
    *_, region, account_id, queue_name = arn.split(":")
    return f"https://sqs.{region}.amazonaws.com/{account_id}/{queue_name}"
