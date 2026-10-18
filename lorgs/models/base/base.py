"""Base Class for all Models in our System."""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
from typing import Any, ClassVar, Self, TypeVar

# IMPORT THIRD PARTY LIBRARIES
import pydantic

# IMPORT LOCAL LIBRARIES
from lorgs import utils


T = TypeVar("T", bound="BaseModel")


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
    def get(cls, **kwargs: Any) -> Self | None:
        ...

    @classmethod
    def get_or_create(cls, **kwargs: Any) -> Self:
        return cls.get(**kwargs) or cls(**kwargs)

    def save(self) -> None:
        ...
