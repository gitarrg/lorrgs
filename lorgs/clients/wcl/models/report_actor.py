# IMPORT THIRD PARTY LIBRARIES
from pydantic import BaseModel


class ReportActor(BaseModel):
    """The ReportActor represents a single player, pet or NPC that occurs in the report."""

    id: int
    """The Source ID of the actor. This ID is used in events to identify sources and targets."""

    name: str = ""
    """The name of the actor."""

    server: str = ""
    """The normalized server name of the actor."""

    type: str = "Player"
    """The type of the actor, i.e., if it is a player, pet or NPC. eg.: "Player", "NPC", "Pet"."""

    subType: str = ""
    """The sub-type of the actor, for players it's their class, and for NPCs, they are further subdivided into normal NPCs and bosses."""

    icon: str = ""
    """An icon to use for the actor. For pets and NPCs, this will be the icon the site chose to represent that actor."""

    # petOwner: typing.Optional[int]
    # """The report ID of the actor's owner if the actor is a pet."""

    # gameID: float
    # """,The game ID of the actor."""
