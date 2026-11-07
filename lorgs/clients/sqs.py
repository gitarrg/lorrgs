"""Client to interact with AWS SQS."""

# IMPORT STANDARD LIBRARIES
import json
import os
import typing
import uuid
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor

# IMPORT THIRD PARTY LIBRARIES
import boto3
from pydantic import BaseModel

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.logger import logger


if typing.TYPE_CHECKING:
    from types_boto3_sqs.type_defs import SendMessageBatchRequestEntryTypeDef


payload_type = str | dict | BaseModel


def _serialize(payload: payload_type) -> str:
    if isinstance(payload, str):
        return payload

    if isinstance(payload, BaseModel):
        return payload.model_dump_json()

    if isinstance(payload, dict):
        return json.dumps(payload)

    # This should never happen
    raise ValueError(f"Invalid payload type: {type(payload)}")


def new_message_group(payload: payload_type = "") -> str:
    """A unique FIFO message group, prefixed with the payload's Game Version.

    The prefix keeps one Game Version's refresh from holding up another's.
    """
    game_version = ""
    if isinstance(payload, dict):
        game_version = payload.get("game_version") or ""
    elif isinstance(payload, BaseModel):
        game_version = getattr(payload, "game_version", "") or ""
    prefix = f"{game_version}-" if game_version else ""
    return f"{prefix}{uuid.uuid4()}"


SQS_CLIENT = boto3.client("sqs")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL") or ""

SQS_LOCAL = os.getenv("SQS_LOCAL", "").lower() in {"1", "true", "yes"}
"""Dev mode: run tasks in this process (with the local code) instead of sending them to AWS."""

_LOCAL_EXECUTOR = ThreadPoolExecutor(max_workers=1, thread_name_prefix="sqs-local")
"""One worker: tasks run one at a time, like a single Lambda sharing the handler's event loop."""


def _run_local(payload: payload_type) -> dict:
    """Run a task with the SQS handler in a background thread. Returns a fake `send_message` response."""
    from lorrgs_sqs import handler  # lazy: the handler imports this module  # ruff: ignore[import-outside-top-level]

    message_id = str(uuid.uuid4())
    record = {"messageId": message_id, "body": _serialize(payload)}

    def run() -> None:
        try:
            handler.handler({"Records": [record]})
        except Exception:  # ruff: ignore[blind-except]
            logger.exception("local task failed")

    _LOCAL_EXECUTOR.submit(run)
    return {"MessageId": message_id}


def send_message(payload: payload_type, queue_url="", message_group=""):
    """Send a single Message."""
    if SQS_LOCAL:
        return _run_local(payload)

    return SQS_CLIENT.send_message(
        QueueUrl=queue_url or SQS_QUEUE_URL,
        MessageGroupId=message_group or new_message_group(payload),
        MessageBody=_serialize(payload),
    )


def send_message_batch(payloads: Iterable[payload_type], queue_url="", chunk_size=10, message_group=""):
    """Batch Submit multiple Messages. Each gets its own FIFO message group, unless `message_group` is given."""
    if SQS_LOCAL:
        for payload in payloads:
            _run_local(payload)
        return

    # Wrap Payloads
    messages: list[SendMessageBatchRequestEntryTypeDef] = [
        {
            "Id": str(i),
            "MessageGroupId": message_group or new_message_group(payload),
            "MessageBody": _serialize(payload),
        }
        for i, payload in enumerate(payloads)
    ]

    # Send
    for entries in utils.chunks(messages, n=chunk_size):
        response = SQS_CLIENT.send_message_batch(
            QueueUrl=queue_url or SQS_QUEUE_URL,
            Entries=entries,
        )
        # SQS reports rejected entries in the response instead of raising
        if failed := response.get("Failed"):
            raise RuntimeError(f"SQS rejected {len(failed)} of {len(entries)} messages: {failed}")
