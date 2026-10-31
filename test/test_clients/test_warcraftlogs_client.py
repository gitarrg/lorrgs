"""Warcraft Logs client turns GraphQL errors into typed exceptions."""

import asyncio
from unittest import mock

import pytest

from lorgs.clients.wcl.client import (
    BaseClient,
    PrivateReportError,
    UnknownReportError,
    WarcraftlogsClient,
    WarcraftlogsQueryError,
)


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


def test_close_instance_closes_the_shared_session() -> None:
    WarcraftlogsClient._instance = None

    async def _close() -> None:
        client = WarcraftlogsClient.get_instance()
        await WarcraftlogsClient.close_instance()
        assert client.session.closed
        assert WarcraftlogsClient._instance is None

    asyncio.run(_close())


def test_other_graphql_messages_raise_query_error_carrying_them() -> None:
    with pytest.raises(WarcraftlogsQueryError) as raised:
        asyncio.run(_query(_graphql_errors("Rate limit exceeded.", "Unknown argument.")))

    assert raised.value.messages == ["Rate limit exceeded.", "Unknown argument."]


################################################################################
# Retries and auth, against a local server


async def _serve(api_responses: list[tuple[int, dict[str, str]]], token_responses: list[tuple[int, dict]]):
    """Start a fake Warcraft Logs answering with the given (status, headers / json) in order."""
    from aiohttp import web
    from aiohttp.test_utils import TestServer

    seen: dict[str, list] = {"api": [], "token": []}

    async def api(request: web.Request) -> web.Response:
        seen["api"].append(request.headers.get("Authorization"))
        status, headers = api_responses.pop(0)
        return web.json_response({"data": {"ok": True}}, status=status, headers=headers)

    async def token(request: web.Request) -> web.Response:
        seen["token"].append(True)
        status, body = token_responses.pop(0)
        return web.json_response(body, status=status)

    app = web.Application()
    app.router.add_route("*", "/api", api)
    app.router.add_post("/token", token)
    server = TestServer(app)
    await server.start_server()
    return server, seen


def _local_client(server, token: str = "old") -> WarcraftlogsClient:
    client = WarcraftlogsClient(client_id="id", client_secret="secret")
    client.URL_API = str(server.make_url("/api"))
    client.URL_AUTH = str(server.make_url("/token"))
    client.headers = {"Authorization": f"Bearer {token}"} if token else {}
    return client


def test_server_errors_and_rate_limits_are_retried() -> None:
    async def run():
        server, seen = await _serve([(503, {}), (429, {"Retry-After": "0"}), (200, {})], [])
        client = _local_client(server)
        with mock.patch("lorgs.clients.wcl.client.asyncio.sleep", mock.AsyncMock()):
            result = await client.query("report { code }")
        await client.close()
        await server.close()
        return result, seen

    result, seen = asyncio.run(run())
    assert result == {"ok": True}
    assert len(seen["api"]) == 3


def test_a_rejected_token_is_refreshed_once() -> None:
    async def run():
        server, seen = await _serve([(401, {}), (200, {})], [(200, {"access_token": "new"})])
        client = _local_client(server)
        result = await client.query("report { code }")
        await client.close()
        await server.close()
        return result, seen

    result, seen = asyncio.run(run())
    assert result == {"ok": True}
    assert seen["api"] == ["Bearer old", "Bearer new"]


def test_failed_auth_raises_and_keeps_no_header() -> None:
    import aiohttp

    async def run():
        server, _ = await _serve([], [(401, {"error": "invalid_client"})])
        client = _local_client(server, token="")
        try:
            with pytest.raises(aiohttp.ClientResponseError):
                await client.query("report { code }")
            return client.headers
        finally:
            await client.close()
            await server.close()

    assert "Authorization" not in asyncio.run(run())
