"""Base for static game data (roles, classes, specs, spells, raids, ...)."""

from __future__ import annotations

# IMPORT LOCAL LIBRARIES
from lorgs.models.base import base


class StaticModel(base.BaseModel):
    """A hand-written game data object, owned by one Game Version's `GameData`."""

    def __hash__(self) -> int:
        # Restore the default implementation because pydantic overwrites it.
        return object.__hash__(self)
