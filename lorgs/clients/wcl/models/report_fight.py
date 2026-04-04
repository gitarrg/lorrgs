from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT THIRD PARTY LIBRARIES
from pydantic import BaseModel, root_validator, validator


class PhaseTransition(BaseModel):
    """A spartan representation of phase transitions during a fight.

    https://www.warcraftlogs.com/v2-api-docs/warcraft/phasetransition.doc.html
    """

    startTime: int
    """The start time of the phase transition. (Milliseconds relative to the start of the report)."""


class ReportFight(BaseModel):
    """The ReportFight represents a single fight that occurs in the report."""

    id: int
    """The report ID of the fight. This ID can be used to fetch only events, tables or graphs for this fight."""

    name: str = ""
    """The name of the fight."""

    startTime: int
    """The start time of the fight. (Milliseconds relative to the start of the report)."""

    endTime: int
    """The end time of the fight. (Milliseconds relative to the start of the report)."""

    inProgress: bool = False
    """Whether or not the fight is still in progress. If this field is false, it means the entire fight has been uploaded."""

    encounterID: int
    """The encounter ID of the fight. If the ID is 0, the fight is considered a trash fight."""

    difficulty: int = 0
    """The difficulty setting for the raid, dungeon, or arena. Null for trash."""

    kill: bool = True
    """Whether or not the fight was a boss kill, i.e., successful. If this field is false, it means the fight was a wipe or a failed run, etc.."""

    bossPercentage: float = 0
    """The percentage health of the active boss or bosses at the end of a fight."""

    fightPercentage: float = 0
    """The actual completion percentage of the fight.
    This is the field used to indicate how far into a fight a wipe was,
    since fights can be complicated and have multiple bosses, no bosses, bosses that heal, etc.
    
    100.0 = Pull / 0.0 = Kill
    """

    phaseTransitions: list[PhaseTransition] = []
    """The start times of the phases in the fight."""

    @root_validator(pre=True)
    def remove_nones(cls, values):
        return {k: v for k, v in values.items() if v is not None}

    @validator("fightPercentage", "bossPercentage")
    def fix_percentage(cls, value: float, values: dict[str, typing.Any]):
        """Set Fight/Boss Percentage for Kills to 0.0

        Sometimes we receive very low values like 0.01-0.04
        for kills rather than exact 0.0.
        """
        kill: bool = values.get("kill", True)
        return 0 if kill else value
