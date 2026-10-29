"""Client to interact with AWS SQS."""

# IMPORT STANDARD LIBRARIES
import json
import os
import uuid
from collections.abc import Iterable

# IMPORT THIRD PARTY LIBRARIES
import boto3
from pydantic import BaseModel

# IMPORT LOCAL LIBRARIES
from lorgs import utils


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


def send_message(payload: payload_type, queue_url="", message_group=""):
    """Send a single Message."""
    return SQS_CLIENT.send_message(
        QueueUrl=queue_url or SQS_QUEUE_URL,
        MessageGroupId=message_group or new_message_group(payload),
        MessageBody=_serialize(payload),
    )


def send_message_batch(payloads: Iterable[payload_type], queue_url="", chunk_size=10):
    """Batch Submit multiple Messages."""
    # Wrap Payloads
    messages = [
        {
            "Id": str(i),
            "MessageGroupId": new_message_group(payload),
            "MessageBody": _serialize(payload),
        }
        for i, payload in enumerate(payloads)
    ]

    # Send
    for entries in utils.chunks(messages, n=chunk_size):
        SQS_CLIENT.send_message_batch(
            QueueUrl=queue_url or SQS_QUEUE_URL,
            Entries=entries,
        )
