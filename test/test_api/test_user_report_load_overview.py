"""Loading a user report surfaces Warcraft Logs access errors."""

import asyncio
import json

import fastapi
import pytest
from fastapi.exception_handlers import http_exception_handler
from starlette.requests import Request

from lorgs.clients.wcl.client import PrivateReportError, WarcraftlogsClient
from lorgs.models.warcraftlogs_user_report import UserReport
from lorrgs_api.routes.api_user_reports import load_user_report_overview


def test_loading_a_private_user_report_returns_a_displayable_error(monkeypatch: pytest.MonkeyPatch) -> None:
    report = UserReport(report_id="privatereport001")
    monkeypatch.setattr(UserReport, "get_or_create", classmethod(lambda cls, **kwargs: report))

    class FakeWarcraftlogsClient:
        async def query(self, query: str) -> dict[str, object]:
            raise PrivateReportError("You do not have permission to view this report.")

    monkeypatch.setattr(WarcraftlogsClient, "get_instance", lambda: FakeWarcraftlogsClient())

    response = asyncio.run(_load_overview())

    assert response.status_code == 401
    assert json.loads(response.body) == {"detail": "No permission to view this report."}


async def _load_overview() -> fastapi.Response:
    try:
        await load_user_report_overview(fastapi.Response(), "privatereport001")
    except fastapi.HTTPException as exc:
        scope = {
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": "GET",
            "scheme": "http",
            "path": "/api/user_reports/privatereport001/load_overview",
            "raw_path": b"/api/user_reports/privatereport001/load_overview",
            "query_string": b"",
            "headers": [],
            "client": ("127.0.0.1", 123),
            "server": ("127.0.0.1", 80),
        }
        return await http_exception_handler(Request(scope), exc)
    raise AssertionError("private report did not return an HTTP error")
