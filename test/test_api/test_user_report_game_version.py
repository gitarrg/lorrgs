"""Seams: a User Report's Game Version comes from its log; the routes stay global."""

from __future__ import annotations

import asyncio
from unittest import mock

import fastapi
import pytest

from lorgs.clients import sqs
from lorgs.models.task import Task
from lorgs.models.warcraftlogs_user_report import UserReport
from lorrgs_api.routes import api_user_reports


def _load(report: UserReport | None) -> dict:
    with (
        mock.patch.object(UserReport, "get", classmethod(lambda cls, **kwargs: report)),
        mock.patch.object(sqs, "send_message", return_value={"MessageId": "m1"}) as send_message,
        mock.patch.object(Task, "save"),
    ):
        asyncio.run(api_user_reports.load_user_report(fastapi.Response(), "abc", fight="1", player="2"))
    return send_message.call_args.kwargs["payload"]


@pytest.mark.parametrize(("wcl_game_version", "expected"), [(1, "retail"), (6, "mists")])
def test_the_queued_task_carries_the_game_version_of_the_log(wcl_game_version: int, expected: str) -> None:
    payload = _load(UserReport(report_id="abc", game_version=wcl_game_version))
    assert payload.game_version == expected


def test_a_log_of_an_unsupported_game_version_is_rejected_naming_it() -> None:
    with pytest.raises(fastapi.HTTPException) as error:
        _load(UserReport(report_id="abc", game_version=5))
    assert error.value.status_code == 422
    assert "5" in error.value.detail


def test_an_unknown_report_is_a_404() -> None:
    with pytest.raises(fastapi.HTTPException) as error:
        _load(None)
    assert error.value.status_code == 404


def test_responses_include_the_game_version_even_for_old_stored_reports() -> None:
    old_item = UserReport.model_validate({"report_id": "abc", "title": "old"})  # stored before game_version existed
    with mock.patch.object(UserReport, "get", classmethod(lambda cls, **kwargs: old_item)):
        report = asyncio.run(api_user_reports.get_user_report("abc"))
    assert report.model_dump(exclude_unset=True)["game_version"] == 1
