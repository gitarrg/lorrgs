"""Base class for all loaders."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import abc
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.clients.wcl import WarcraftlogsClient


if typing.TYPE_CHECKING:
    from lorgs.models.game_data import GameData


class BaseLoader:
    """Base class for all loaders."""

    def __init__(self, game_data: GameData) -> None:
        self.game_data = game_data

    @abc.abstractmethod
    def get_query(self) -> str:
        """Get the query for the loader."""

    @abc.abstractmethod
    def process_query_result(self, query_result: dict[str, typing.Any]) -> None:
        """Process the query result."""

    def needs_load(self) -> bool:  # ruff: ignore[no-self-use]
        """Check if the data needs to be loaded."""
        return True

    async def load(self, client: WarcraftlogsClient | None = None) -> None:
        """Load the data."""
        query = self.get_query()
        if not query:
            return

        if not client:
            client = WarcraftlogsClient.get_instance()

        result = await client.query(query)
        if not result:
            return

        self.process_query_result(result)
