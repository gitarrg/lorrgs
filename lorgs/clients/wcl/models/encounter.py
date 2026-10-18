# IMPORT THIRD PARTY LIBRARIES
from pydantic import BaseModel

# IMPORT LOCAL LIBRARIES
from .character_ranking import CharacterRankings
from .fight_rankings import FightRankings
from .zone import Zone


class Encounter(BaseModel):
    """A single encounter for the game.."""

    id: int = 0
    """The ID of the encounter."""

    name: str = ""
    """The localized name of the encounter."""

    zone: Zone | None = None
    """The zone that this encounter is found in."""

    characterRankings: CharacterRankings = CharacterRankings()
    """Player rankings information for a encounter."""

    fightRankings: FightRankings = FightRankings()
    """Fight rankings information for a zone."""
