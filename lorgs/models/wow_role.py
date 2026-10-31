"""Models for a Role in the Game."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

import pydantic

# IMPORT LOCAL LIBRARIES
from lorgs.models import base


if typing.TYPE_CHECKING:
    from lorgs.models.wow_spec import WowSpec  # ruff: ignore[runtime-import-in-type-checking-block]  # only a PrivateAttr annotation


class WowRole(base.StaticModel):
    """A role like Tank, Healer, DPS."""

    id: int  # used for sorting

    name: str
    """Full Name of the role. eg.: "Healer"."""

    code: str
    """Lowercase short Version. eg.: `tank`, `heal`, `mdps` or `rdps`."""

    metric: str = "dps"
    """Default Metric. dps for all. hps for healers."""

    metrics: list[str] = ["dps", "hps", "bossdps"]

    playable: bool = True
    """False for pseudo-roles whose specs are spell groups (eg.: Items), not something a player can be."""

    _specs: set[WowSpec] = pydantic.PrivateAttr(default_factory=set)

    @property
    def specs(self) -> set[WowSpec]:
        """The Specs of this Role. Each Spec registers itself when it is created."""
        return self._specs

    def register_spec(self, spec: WowSpec) -> None:
        self._specs.add(spec)

    def __lt__(self, other: WowRole) -> bool:
        return self.id < other.id

    def as_dict(self) -> dict[str, typing.Any]:
        specs_sorted = sorted(self.specs)
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "specs": [spec.full_name_slug for spec in specs_sorted],
            "spec_ids": [spec.id for spec in specs_sorted],
            "metrics": self.metrics,
            "playable": self.playable,
        }
