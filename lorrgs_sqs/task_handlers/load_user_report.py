"""Handler to Load User Reports.

to be triggered via SQS

"""
from __future__ import annotations

# IMPORT LOCAL LIBRARIES
from lorgs import data  # pylint: disable=unused-import  # noqa: F401
from lorgs.loaders.report_loader import ReportLoader
from lorgs.logger import logger
from lorgs.models import warcraftlogs_actor
from lorgs.models.task import Task
from lorgs.models.task_payloads import UserReportPayload
from lorgs.models.warcraftlogs_user_report import UserReport
from lorrgs_sqs.exceptions import TaskValidationError


def set_task_item_status(task: Task):
    """Create a Callback to update an Item in Task."""

    # map event names to task status
    event_to_status = {
        "start": task.STATUS.IN_PROGRESS,
        "failed": task.STATUS.FAILED,
        "success": task.STATUS.DONE,
    }

    def handler(actor: warcraftlogs_actor.BaseActor, status: str) -> None:
        # actor: typing.Optional["warcraftlogs_actor.BaseActor"] = event.payload.get("actor")
        if not actor:
            return

        fight_id = actor.fight.fight_id if actor.fight else 0
        source_id = actor.source_id
        if (fight_id <= 0) or (source_id <= 0):
            return

        status = event_to_status.get(status, status)
        task.set(**{f"items.{fight_id}_{source_id}.status": status})

    return handler


async def load_user_report(payload: UserReportPayload) -> None:
    logger.info(f"load_user_report: {payload}")

    ################################
    # loading...
    user_report = UserReport.get_or_create(report_id=payload.report_id)

    report_loader = ReportLoader(report=user_report)
    await report_loader.load(fight_ids=payload.fight_ids, player_ids=payload.player_ids)
    user_report.save()


async def main(message: dict[str, str]) -> None:

    # task status Updates
    message_id = message.get("messageId")
    task = Task.get_or_create(task_id=message_id)
    task.set(status=task.STATUS.IN_PROGRESS)

    task_updater = set_task_item_status(task)
    warcraftlogs_actor.BaseActor.event_actor_load.connect(task_updater)

    # parse input
    message_body = message.get("body")
    if not message_body:
        raise TaskValidationError("No message body.")
    payload = UserReportPayload.model_validate_json(message_body, extra="ignore")

    # Main
    try:
        await load_user_report(payload)
    except:
        task.set(status=task.STATUS.FAILED)
        raise
    else:
        task.set(status=task.STATUS.DONE)
