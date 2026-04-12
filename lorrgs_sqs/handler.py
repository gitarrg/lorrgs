from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import asyncio
import json
import typing
import uuid

# IMPORT THIRD PARTY LIBRARIES
import boto3

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.logger import logger
from lorrgs_sqs import helpers
from lorrgs_sqs.exceptions import TaskValidationError
from lorrgs_sqs.task_handlers import load_comp_rankings, load_spec_rankings, load_user_report, send_discord_message


TASK_HANDLERS = {
    # for debugging
    "unknown": send_discord_message.main,
    "discord": send_discord_message.main,
    "load_user_report": load_user_report.main,
    "load_spec_rankings": load_spec_rankings.main,
    "load_comp_rankings": load_comp_rankings.main,
}


SQS_CLIENT = boto3.client("sqs")


loop = asyncio.new_event_loop()
"""A global loop shared across multiple invokations of the same lambda.

This is required when lambda reuses the same instance for subsequent runs
"""


def submit_messages(queue_url: str, messages: list[dict], chunk_size: int = 10) -> None:
    """Submit messages to the queue in chunks."""
    logger.info(f"submit_messages: {messages=}")

    # Inject IDs
    messages = [{"Id": str(i), **msg} for i, msg in enumerate(messages)]

    for entries in utils.chunks(messages, n=chunk_size):
        logger.info(f"entries: {entries=}")
        response = SQS_CLIENT.send_message_batch(
            QueueUrl=queue_url,
            Entries=entries,  # type: ignore
        )
        logger.info(f"response: {response=}")


async def process_message(message: dict) -> None:
    """Process a single message."""

    payload = json.loads(message.get("body") or "")
    task = payload.get("task") or "unknown"

    #################################
    # See if the message expands into multiple tasks
    # if so: resubmit those back to the queue
    payloads = helpers.expand_keywords(payload)
    if len(payloads) > 1:
        queue_url = helpers.queue_arn_to_url(message.get("eventSourceARN", ""))

        messages = [{"MessageBody": json.dumps(payload), "MessageGroupId": str(uuid.uuid4())} for payload in payloads]

        return submit_messages(queue_url, messages)

    #################################
    # run the Handler
    handler = TASK_HANDLERS.get(task) or TASK_HANDLERS["unknown"]
    await handler(message)


async def process_messages(messages: typing.List) -> dict[str, typing.Any]:
    """Wrapper to process all messages in the batch."""
    failures: list[str] = []

    for message in messages:
        try:
            await process_message(message)
        except TaskValidationError:
            logger.warning("Validation error processing message", exc_info=True)
        except Exception:
            logger.exception("Error processing message")
            failures.append(message.get("MessageId"))

    return {
        "batchItemFailures": [f for f in failures if f],
    }


def handler(event, context=None) -> None:
    """Main Handler called by Lambda."""
    logger.info(f"handler: {event=}")
    records = event.get("Records") or []

    # We can not use `asyncio.run` here as it creates and closes fresh loop
    # each time it runs.
    # This interferes with shared instances (eg.: the `aiohttp.ClientSession`)
    # that are bound to a given loop.
    loop.run_until_complete(process_messages(records))

    logger.info("handler done.")
