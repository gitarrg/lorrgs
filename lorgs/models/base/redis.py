"""Basic Client to store Objects in a Redis DB."""

# IMPORT STANDARD LIBRARIES
import json
import os
from typing import Any, ClassVar, Optional, Type, TypeVar

# IMPORT THIRD PARTY LIBRARIES
import redis

# IMPORT LOCAL LIBRARIES
from lorgs.models.base import base


REDIS_URL = os.getenv("REDIS_URL") or "redis://localhost:6379"


redis_client = redis.from_url(REDIS_URL)


TRedisModel = TypeVar("TRedisModel", bound="RedisModel")


class RedisModel(base.BaseModel):

    ttl: ClassVar[int] = 0

    ############################################################################
    # GET
    #

    @classmethod
    def get(cls: Type[TRedisModel], **kwargs: Any) -> Optional[TRedisModel]:
        """Get a Object using its Key."""
        key = cls.get_key(**kwargs)
        data = redis_client.json().get(key) or {}
        if data:
            return cls(**data)
        else:
            return None

    ############################################################################
    # SET
    #

    def save(self, exclude_unset=True, **kwargs: Any) -> None:
        """Save the Object."""
        key = self.get_key(**self.model_dump())

        # Use pydantics json encoder to convert complex types (eg.: datetime)
        data = json.loads(self.model_dump_json(exclude_unset=exclude_unset, **kwargs))

        redis_client.json().set(name=key, path=".", obj=data)

        if self.ttl:
            redis_client.expire(key, self.ttl)

    def set(self, **kwargs: Any) -> None:
        """Update values on the Object,

        Todo:
            reload/update the instance itself
        """
        key = self.get_key(**self.model_dump())
        for path, value in kwargs.items():
            if not path.startswith("."):
                path = f".{path}"

            redis_client.json().set(name=key, path=path, obj=value)
