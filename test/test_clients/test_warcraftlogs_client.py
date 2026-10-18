"""Warcraft Logs client turns GraphQL errors into typed exceptions."""

import asyncio
from unittest import mock

import pytest

from lorgs.clients.wcl.client import BaseClient, PrivateReportError, UnknownReportError, WarcraftlogsClient, WarcraftlogsQueryError


PRIVATE_REPORT_MESSAGE = "You do not have permission to view this report."
UNKNOWN_REPORT_MESSAGE = "This report does not exist."


def _client() -> WarcraftlogsClient:
    return WarcraftlogsClient.__new__(WarcraftlogsClient)


def _graphql_errors(*messages: str) -> dict[str, list[dict[str, str]]]:
    return {"errors": [{"message": message} for message in messages]}


async def _query(result: dict[str, list[dict[str, str]]]) -> dict[str, object]:
    client = _client()
    client.raise_errors = False

    async def transport(self: BaseClient, url: str, query: str) -> dict[str, list[dict[str, str]]]:
        return result

    with mock.patch.object(BaseClient, "query", transport):
        return await client.query("report { code }")


def test_private_report_message_raises_even_when_a_caller_disables_errors() -> None:
    with pytest.raises(PrivateReportError):
        asyncio.run(_query(_graphql_errors(PRIVATE_REPORT_MESSAGE)))


def test_missing_report_message_raises_unknown_report() -> None:
    with pytest.raises(UnknownReportError):
        asyncio.run(_query(_graphql_errors(UNKNOWN_REPORT_MESSAGE)))


def test_other_graphql_messages_raise_query_error_carrying_them() -> None:
    with pytest.raises(WarcraftlogsQueryError) as raised:
        asyncio.run(_query(_graphql_errors("Rate limit exceeded.", "Unknown argument.")))

    assert raised.value.messages == ["Rate limit exceeded.", "Unknown argument."]
