"""Warcaftlogs API Client."""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import asyncio
import os
import typing

# IMPORT THIRD PARTY LIBRARIES
import aiohttp

# IMPORT LOCAL LIBRARIES
from lorgs.logger import logger, timeit


# error text we get from Warcraftlogs if a report does not exist.
ERROR_MESSAGE_INVALID_REPORT = "This report does not exist."
ERROR_MESSAGE_PRIVATE_REPORT = "You do not have permission to view this report."


class InvalidReport(ValueError):
    """Exception raised when a report was not found."""


class UnknownReportError(InvalidReport):
    """The report was deleted or never existed."""


class PrivateReportError(Exception):
    """The report exists, but Warcraft Logs refused access to it."""


class WarcraftlogsQueryError(Exception):
    """Warcraft Logs returned GraphQL errors that are not a known report state."""

    def __init__(self, messages: list[str]) -> None:
        self.messages = messages
        super().__init__("\n".join(messages))


T = typing.TypeVar("T", bound="BaseClient")


CONCURRENT_CONNECTIONS = int(os.getenv("CONCURRENT_CONNECTIONS") or 10)
"""int: Number of parallel Requests."""


class BaseClient:

    _sem = asyncio.Semaphore(value=CONCURRENT_CONNECTIONS)
    """Semaphore used to control the number of parallel Requests."""

    # reference used to provide a singelton interface.
    _instance: typing.Self | None = None

    @classmethod
    def get_instance(cls, *args: typing.Any, **kwargs: typing.Any) -> typing.Self:
        """Get an instance of the Client.

        This is a singleton-style wrapper,
        which will return an existing instance, if there is one,
        or create a new instance otherwise.

        Args:
            *args: passed to the __init__
            **kwargs: passed to the __init__

        Returns:
            <BaseClient> instance.

        """
        if cls._instance is None:
            logger.debug(f"creating new {cls.__name__} Instance.")
            cls._instance = cls(*args, **kwargs)  # ty:ignore[invalid-assignment]
        return cls._instance

    @classmethod
    async def close_instance(cls) -> None:
        """Close and drop the shared client, if one was created."""
        instance = cls._instance
        cls._instance = None
        if instance is not None:
            await instance.close()

    def __init__(self) -> None:
        self.headers: dict[str, typing.Any] = {}
        # self.session: typing.Optional[aiohttp.ClientSession] = None
        session_timeout = aiohttp.ClientTimeout(total=60)
        conn = aiohttp.TCPConnector(limit_per_host=CONCURRENT_CONNECTIONS)
        self.session = aiohttp.ClientSession(connector=conn, timeout=session_timeout)

    async def close(self) -> None:
        """Close the HTTP session and its connector."""
        if not self.session.closed:
            await self.session.close()

    async def ensure_auth(self) -> None:
        """Ensure the Client is authenticated prior making any Requests."""

    @timeit
    async def query(self, url: str, query: str) -> typing.Any:
        """Executes a "query" to "url".

        reuses a shared ClientSession and limits the maximum number of
        parallel connections

        Args:
            url (str): the url to execute the query on
            query (str): the query to execute

        """
        await self.ensure_auth()
        async with self.session.get(url=url, json={"query": query}, headers=self.headers) as resp:
            resp.raise_for_status()
            return await resp.json()


class WarcraftlogsClient(BaseClient):

    URL_API = "https://www.warcraftlogs.com/api/v2/client"
    URL_AUTH = "https://www.warcraftlogs.com/oauth/token"

    def __init__(self, client_id: str = "", client_secret: str = "") -> None:
        super().__init__()

        # credentials
        self.client_id = client_id or os.getenv("WCL_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("WCL_CLIENT_SECRET")
        self.headers: dict[str, str] = {}

        auth_token = os.getenv("WCL_AUTH_TOKEN")
        if auth_token:
            self.headers["Authorization"] = "Bearer " + auth_token

        logger.info("NEW CLIENT: %s", self.client_id)
        self._num_queries = 0

    ################################
    #   Connection
    #

    async def update_auth_token(self) -> None:
        """Request a new Auth Token from Warcraftlogs."""
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        logger.debug("Auth: %s", self.client_id)
        async with aiohttp.ClientSession() as session, session.post(url=self.URL_AUTH, data=data) as resp:
            try:
                response: dict[str, str] = await resp.json()
            except Exception:
                logger.error(resp.text())
                raise

        token = response.get("access_token", "")
        self.headers["Authorization"] = "Bearer " + token

    async def ensure_auth(self) -> None:
        if self.headers.get("Authorization"):
            return
        await self.update_auth_token()

    async def get_rate_info(self) -> dict[str, int]:
        query = """
        rateLimitData
        {
            pointsSpentThisHour
            limitPerHour
            pointsResetIn
        }
        """
        result = await self.query(query)
        return result.get("rateLimitData") or {}

    async def get_points_left(self) -> int:
        """Points left until we hit the rate limit."""
        info = await self.get_rate_info()
        return info.get("limitPerHour", 0) - info.get("pointsSpentThisHour", 0)

    @staticmethod
    def _raise_errors(result: dict[str, typing.Any]) -> None:
        if result.get("error"):
            raise WarcraftlogsQueryError([str(result["error"])])

        messages: list[str] = []
        for error in result.get("errors") or []:
            message = error.get("message") or ""
            if message == ERROR_MESSAGE_INVALID_REPORT:
                raise UnknownReportError(message)
            if message == ERROR_MESSAGE_PRIVATE_REPORT:
                raise PrivateReportError(message)
            if message:
                messages.append(message)
        if messages:
            raise WarcraftlogsQueryError(messages)

    async def query(self, query: str) -> dict[str, typing.Any]:

        # Format Inputs
        if not query:
            return {}
        query = f"query {{ {query} }}"

        # Run
        result = await super().query(self.URL_API, query)

        self._raise_errors(result)
        return result.get("data", {})

    async def multiquery(self, queries: list[str], *args: typing.Any, **kwargs: typing.Any) -> list[typing.Any]:
        """Execute a list of queries as a batch.

        Args:
            queries: the queries to run
            *args: passed to the query
            **kwargs: passed to the query

        Returns:
            data[object]: the results in the same order

        """
        tasks = [self.query(query, *args, **kwargs) for query in queries]
        return await asyncio.gather(*tasks)
