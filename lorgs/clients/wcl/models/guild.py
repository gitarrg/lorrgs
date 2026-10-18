from pydantic import BaseModel


class Guild(BaseModel):
    """A single guild. Guilds earn their own rankings and contain characters.

    They may correspond to a guild in-game or be a custom guild created just to hold reports and rankings.
    """

    id: int = 0
    """The ID of the guild."""

    name: str = ""
    """The name of the guild."""
