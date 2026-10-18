from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
from pydantic import BaseModel, root_validator


class UnitInfo(BaseModel):
    name: str
    """Unit Name. eg,.: Charater- or NPC-Name."""
    id: int
    """Source ID."""
    guid: int = 0
    """Units GUID"""
    type: str
    """Unit Type. ClassName for Players."""


class PlayerTotal(UnitInfo):
    """Per Player Name and Total."""

    total: int = 0


################################################################################


class DeathEventAbility(BaseModel):
    name: str = ""
    """Name of the Ability."""
    type: int = 0
    """DMG Type."""
    abilityIcon: str = ""

    guid: int = 0
    """Spell ID."""


class DeathEvent(UnitInfo):
    """Event describing a players death."""

    deathTime: int
    ability: DeathEventAbility = DeathEventAbility(name="")


################################################################################


class CompositionEntrySpec(BaseModel):
    spec: str
    role: str = ""


class CompositionEntry(UnitInfo):
    specs: list[CompositionEntrySpec]


################################################################################


class ReportSummary(BaseModel):

    totalTime: int = 0
    itemLevel: float = 0
    composition: list[CompositionEntry] = []
    damageDone: list[PlayerTotal] = []
    healingDone: list[PlayerTotal] = []
    deathEvents: list[DeathEvent] = []

    @root_validator(pre=True)
    def unwrap_data(cls, v):
        if v and v.get("data"):
            v = v["data"]
        return v
