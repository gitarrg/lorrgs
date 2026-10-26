from __future__ import annotations

from collections.abc import Callable
from typing import Any

from lorgs.data import CURRENT_SEASON
from lorgs.data.roles import ALL_ROLES
from lorgs.game_version import ACTIVE
from lorgs.models.wow_role import WowRole
from lorgs.models.wow_spec import WowSpec


def expand_metric(payload: dict) -> list[str]:
    spec_slug = payload.get("spec_slug", "")

    spec = WowSpec.get(full_name_slug=spec_slug)
    role = (spec and spec.role) or WowRole.get(code="tank")
    return (role and role.metrics) or []


ALL_SPECS = {spec for role in ALL_ROLES for spec in role.specs}  # class specs only, no item pseudo-specs
ALL_BOSSES = []
for raid in CURRENT_SEASON.raids:
    ALL_BOSSES.extend(raid.bosses)


PAYLOAD_EXPANDERS: dict[str, list[str] | Callable[[Any], list[str]]] = {
    "spec_slug": [spec.full_name_slug for spec in ALL_SPECS],
    "boss_slug": [boss.full_name_slug for boss in ALL_BOSSES],
    "difficulty": list(ACTIVE.difficulty_names),
    "metric": expand_metric,
}


def expand_payload(keyword: str, payload: dict) -> list[dict]:
    if payload.get(keyword) != "all":
        return [payload]

    values = PAYLOAD_EXPANDERS[keyword]
    if callable(values):
        values = values(payload)

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
