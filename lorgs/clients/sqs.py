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


SQS_CLIENT = boto3.client("sqs")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL") or ""


def send_message(payload: payload_type, queue_url="", message_group=""):
    """Send a single Message."""
    message_group = message_group or str(uuid.uuid4())
    return SQS_CLIENT.send_message(
        QueueUrl=queue_url or SQS_QUEUE_URL,
        MessageGroupId=message_group,
        MessageBody=_serialize(payload),
    )


def send_message_batch(payloads: Iterable[payload_type], queue_url="", chunk_size=10):
    """Batch Submit multiple Messages."""

    # Wrap Payloads
    messages = [
        {
            "Id": str(i),
            "MessageGroupId": str(uuid.uuid4()),
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
