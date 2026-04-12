"""Base class for all loaders."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import abc
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.clients.wcl import WarcraftlogsClient


class BaseLoader:
    """Base class for all loaders."""

    @abc.abstractmethod
    def get_query(self) -> str:
        """Get the query for the loader."""
        return ""

    @abc.abstractmethod
    def process_query_result(self, query_result: dict[str, typing.Any]) -> None:
        """Process the query result."""
        raise NotImplementedError

    async def load(
        self,
        client: WarcraftlogsClient | None = None,
        *,
        raise_errors: bool = False,
    ) -> None:
        """Load the data."""
        query = self.get_query()

        if not client:
            client = WarcraftlogsClient.get_instance()

        result = await client.query(query, raise_errors=raise_errors)
        self.process_query_result(result)
