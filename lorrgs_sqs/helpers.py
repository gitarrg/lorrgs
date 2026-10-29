from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.data import GAME_VERSIONS
from lorgs.models import selectors
from lorrgs_sqs.exceptions import TaskValidationError


if typing.TYPE_CHECKING:
    from collections.abc import Callable

    from lorgs.models.game_data import GameData


def get_game_data(payload: dict) -> GameData:
    """The Game Data of the Game Version the payload belongs to."""
    name = payload.get("game_version")
    if name not in GAME_VERSIONS:
        raise TaskValidationError(f"Invalid game_version: {name!r}")
    return GAME_VERSIONS[name].data


def expand_spec_slug(payload: dict) -> list[str]:
    return [spec.full_name_slug for spec in selectors.select_specs(get_game_data(payload), selectors.ALL)]


def expand_boss_slug(payload: dict) -> list[str]:
    return [boss.full_name_slug for boss in selectors.select_bosses(get_game_data(payload), selectors.ALL)]


def expand_metric(payload: dict) -> list[str]:
    spec = get_game_data(payload).get_spec(payload.get("spec_slug", ""))
    return selectors.select_metrics(spec, selectors.ALL)


def expand_difficulty(payload: dict) -> list[str]:
    return selectors.select_difficulties(get_game_data(payload), payload.get("boss_slug", ""), selectors.ALL)


PAYLOAD_EXPANDERS: dict[str, Callable[[typing.Any], list[str]]] = {
    "spec_slug": expand_spec_slug,
    "boss_slug": expand_boss_slug,
    "difficulty": expand_difficulty,
    "metric": expand_metric,
}


def expand_payload(keyword: str, payload: dict) -> list[dict]:
    if payload.get(keyword) != selectors.ALL:
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
