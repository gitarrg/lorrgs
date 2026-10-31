"""Model to Store Task Status."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import datetime
import typing

# IMPORT THIRD PARTY LIBRARIES
import pydantic

# IMPORT LOCAL LIBRARIES
from lorgs.models.base import redis


class Task(redis.RedisModel):
    class STATUS:
        NEW = "new"
        WAITING = "waiting"
        IN_PROGRESS = "in-progress"
        DONE = "done"
        FAILED = "failed"

    task_id: str = ""
    status: str = STATUS.NEW
    updated: datetime.datetime = pydantic.Field(default_factory=lambda: datetime.datetime.now(datetime.UTC))
    message: str = ""
    items: dict[str, typing.Any] = {}

    # Config

    key: typing.ClassVar[str] = "{table_name}:{task_id}"
    # expire time for the tasks (1 hour)
    ttl: typing.ClassVar[int] = 60 * 60
