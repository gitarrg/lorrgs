from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
from pydantic import BaseModel, ValidationInfo, field_validator, model_validator


class PhaseTransition(BaseModel):
    """A spartan representation of phase transitions during a fight.

    https://www.warcraftlogs.com/v2-api-docs/warcraft/phasetransition.doc.html
    """

    id: int = 0
    """The 1-indexed id of the phase. Phase IDs are absolute within a fight: phases with the same ID correspond to the same semantic phase."""

    startTime: int
    """The start time of the phase transition. (Milliseconds relative to the start of the report)."""


class ReportDungeonPull(BaseModel):
    """A pull inside a dungeon run: trash, or a boss fight when `encounterID` is set.

    https://www.warcraftlogs.com/v2-api-docs/warcraft/reportdungeonpull.doc.html
    """

    id: int = 0
    encounterID: int = 0
    """The encounter id if the pull is a boss. 0 for trash."""

    name: str = ""
    """Name of the boss (or of the pull's first enemy for trash)."""

    startTime: float = 0
    """Milliseconds relative to the start of the report."""

    endTime: float = 0
    """Milliseconds relative to the start of the report."""

    @model_validator(mode="before")
    @classmethod
    def remove_nones(cls, values):
        return {k: v for k, v in values.items() if v is not None}


class ReportFight(BaseModel):
    """The ReportFight represents a single fight that occurs in the report."""

    id: int = -1
    """The report ID of the fight. This ID can be used to fetch only events, tables or graphs for this fight."""

    name: str = ""
    """The name of the fight."""

    startTime: int = 0
    """The start time of the fight. (Milliseconds relative to the start of the report)."""

    endTime: int = 0
    """The end time of the fight. (Milliseconds relative to the start of the report)."""

    inProgress: bool = False
    """Whether or not the fight is still in progress. If this field is false, it means the entire fight has been uploaded."""

    encounterID: int = 0
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

    dungeonPulls: list[ReportDungeonPull] = []
    """The pulls of a dungeon run. Empty for everything else."""

    keystoneLevel: int = 0
    """The Mythic+ keystone level. 0 outside of Mythic+ runs."""

    keystoneTime: int = 0
    """The Mythic+ run time in milliseconds. 0 outside of Mythic+ runs."""

    keystoneBonus: int = 0
    """Mythic+ upgrade: 0 = depleted, 1/2/3 = timed at +1/+2/+3."""

    keystoneAffixes: list[int] = []
    """The Mythic+ affix ids."""

    friendlyPlayers: list[int] = []
    """The IDs of all friendly players that took part in the fight (the Report's actor ids)."""

    @model_validator(mode="before")
    @classmethod
    def remove_nones(cls, values):
        return {k: v for k, v in values.items() if v is not None}

    @field_validator("fightPercentage", "bossPercentage")
    @classmethod
    def fix_percentage(cls, value: float, info: ValidationInfo):
        """Set Fight/Boss Percentage for Kills to 0.0.

        Sometimes we receive very low values like 0.01-0.04
        for kills rather than exact 0.0.
        """
        kill: bool = info.data.get("kill", True)
        return 0 if kill else value
