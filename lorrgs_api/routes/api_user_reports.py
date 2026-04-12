"""Routes related to UserReports."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import itertools
import os

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.clients import sqs
from lorgs.clients.wcl import InvalidReport
from lorgs.models.task import Task
from lorgs.models.task_payloads import UserReportPayload
from lorgs.models.warcraftlogs_user_report import UserReport


router = fastapi.APIRouter()


SQS_USER_QUEUE_URL = os.getenv("SQS_USER_QUEUE_URL") or ""


@router.get("/{report_id}", response_model_exclude_unset=True)
async def get_user_report(report_id: str) -> UserReport:
    """Returns the overview about a user report."""
    user_report = UserReport.get(report_id=report_id, create=False)
    if not user_report:
        raise fastapi.HTTPException(status_code=404, detail="Report not found.")

    # TODO: exclude nested casts/fights etc
    return user_report


@router.get("/{report_id}/fights")
async def get_fights(report_id: str, fight: str, player: str = ""):
    """Get Fights in a report.

    Args:
        report_id: id of the report to load (code/id from the warcraftlogs url)
        fight (str): dot separated list of fight ids (eg.: 2.4.15)
        player (str): dot separated list of player ids (eg.: 1.5.20)

    """
    user_report = UserReport.get(report_id=report_id, create=False)
    if not user_report:
        raise fastapi.HTTPException(status_code=404, detail="Report not found.")

    fight_ids = utils.str_int_list(fight)
    player_ids = utils.str_int_list(player)

    fights = user_report.get_fights(*fight_ids)

    for f in fights:
        f.players = f.get_players(*player_ids)

    return {"fights": [fight.model_dump(exclude_unset=True, by_alias=True) for fight in fights]}


################################################################################


@router.get("/{report_id}/load_overview", response_model_exclude_unset=True)
async def load_user_report_overview(response: fastapi.Response, report_id: str, refresh: bool = False) -> UserReport:
    """Load a Report's Overview/Masterdata."""
    response.headers["Cache-Control"] = "max-age=60"

    user_report = UserReport.get_or_create(report_id=report_id)

    needs_to_load = refresh or not user_report.is_loaded
    if needs_to_load:
        try:
            await user_report.load(raise_errors=True)
        except InvalidReport:
            raise fastapi.HTTPException(status_code=404, detail="Report not found.")
        except PermissionError:
            raise fastapi.HTTPException(status_code=401, detail="No permission to view this report.")
        else:
            user_report.save()

    return user_report


@router.get("/{report_id}/load")
async def load_user_report(response: fastapi.Response, report_id: str, fight: str, player: str, user_id: int = 0):
    """Load a Report

    Args:
        report_id(str): the report to load
        fight (str): dot separated list of fight ids (eg.: 2.4.15)
        player (str): dot separated list of player ids (eg.: 1.5.20)
        user_id (int, optional): user id to identify logged in users

    """
    response.headers["Cache-Control"] = "no-cache"

    fight_ids = utils.str_int_list(fight)
    player_ids = utils.str_int_list(player)

    payload = UserReportPayload(
        report_id=report_id,
        user_id=user_id,
        fight_ids=fight_ids,
        player_ids=player_ids,
    )

    message = sqs.send_message(queue_url=SQS_USER_QUEUE_URL, payload=payload)
    message_id = message["MessageId"]

    # task object to help track the progress
    task = Task(task_id=message_id, status=Task.STATUS.WAITING)

    # Add subitems to track the status more granular
    for f, p in itertools.product(fight_ids, player_ids):
        task.items[f"{f}_{p}"] = {"fight": f, "player": p, "status": task.status}

    task.save()

    return {
        "task_id": message_id,
        "queue": "aws",
    }
