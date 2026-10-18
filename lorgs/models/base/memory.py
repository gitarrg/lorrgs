"""Object store in Memory.

This model keeps a reference to all its instance in memory using a weakref-set,
proving us with database-like access to the objects.

"""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
from collections import defaultdict
from typing import ClassVar, Self, TypeVar
from weakref import WeakSet

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models.base import base


T = TypeVar("T", bound="MemoryModel")


class MemoryModel(base.BaseModel):
    """Model which keeps track of all created instances in memory."""

    # dict to track created instances.
    # keys = ModelClass / Values = Set of Instances
    __instances__: ClassVar[defaultdict] = defaultdict(WeakSet)

    def post_init(self) -> None:
        super().post_init()
        self.__instances__[type(self)].add(self)

    @classmethod
    def get(cls, **kwargs) -> Self | None:
        instances = cls.__instances__[cls]
        return utils.get(instances, **kwargs)

    @classmethod
    def list(cls) -> list[Self]:
        return list(cls.__instances__[cls])

    def __hash__(self) -> int:
        # Restore the default implementation because pydantic overwrites it.
        return object.__hash__(self)
