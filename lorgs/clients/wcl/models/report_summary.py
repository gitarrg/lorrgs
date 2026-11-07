from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
from typing import Any

from pydantic import BaseModel, model_validator


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


class PlayerTalent(BaseModel):
    id: int
    """Talent node *entry* id (same ids as `CharacterRankingTalent.talentID`)."""
    rank: int = 1


class PlayerDetail(BaseModel):
    id: int
    """Source ID."""
    talents: list[PlayerTalent] = []
    """Talent choices (`combatantInfo.talentTree`). Empty if Warcraft Logs has none for the player."""

    @model_validator(mode="before")
    @classmethod
    def flatten_combatant_info(cls, data: Any) -> Any:
        """`combatantInfo` is a dict, or an empty list when unknown. Keep the real talent entries (with an `id`)."""
        if not isinstance(data, dict):
            return data
        info = data.get("combatantInfo")
        tree = info.get("talentTree") if isinstance(info, dict) else None
        if not isinstance(tree, list):
            tree = []
        return {"id": data.get("id"), "talents": [t for t in tree if isinstance(t, dict) and t.get("id")]}


class ReportSummary(BaseModel):
    totalTime: int = 0
    itemLevel: float = 0
    composition: list[CompositionEntry] = []
    damageDone: list[PlayerTotal] = []
    healingDone: list[PlayerTotal] = []
    deathEvents: list[DeathEvent] = []
    playerDetails: dict[str, list[PlayerDetail]] = {}
    """Per role (`tanks`, `healers`, `dps`)."""
