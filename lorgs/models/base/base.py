"""Base Class for all Models in our System."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import datetime
from typing import Annotated, Any, ClassVar, Self, TypeVar

# IMPORT THIRD PARTY LIBRARIES
import pydantic

# IMPORT LOCAL LIBRARIES
from lorgs import utils


T = TypeVar("T", bound="BaseModel")


def as_utc(value: datetime.datetime) -> datetime.datetime:
    """Treat a timestamp without a timezone as UTC."""
    if value.tzinfo is None:
        return value.replace(tzinfo=datetime.UTC)
    return value


UTCDatetime = Annotated[datetime.datetime, pydantic.AfterValidator(as_utc)]
"""A timezone-aware datetime. Naive values (stored by older versions) are read as UTC."""

UTC_MIN = datetime.datetime.min.replace(tzinfo=datetime.UTC)
"""The earliest timezone-aware datetime: default for "never updated"."""


class BaseModel(pydantic.BaseModel):
    """Base Class for all Models in our System."""

    key: ClassVar[str] = "{id}"

    def post_init(self) -> None:
        """Hook to implement some custom initialization logic."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.post_init()

    @classmethod
    def get_table_name(cls) -> str:
        return utils.to_snake_case(cls.__name__)

    @classmethod
    def get_key(cls, **kwargs) -> str:
        """Generate a `key` based on the given `kwargs`."""
        kwargs.setdefault("table_name", cls.get_table_name())
        return cls.key.format(**kwargs)

    @classmethod
    def get(cls, **kwargs: Any) -> Self | None: ...

    @classmethod
    def get_or_create(cls, **kwargs: Any) -> Self:
        return cls.get(**kwargs) or cls(**kwargs)

    def save(self) -> None: ...
