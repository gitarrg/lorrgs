"""Get Information about Tasks."""
from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
import asyncio
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs.models.task import Task


router = fastapi.APIRouter(tags=["tasks"], prefix="/tasks")


def _get_task_info(task_id: str) -> dict:
    task = Task.get(task_id=task_id)
    if not task:
        raise KeyError("Task not found")

    return {
        "task_id": task.key,
        "status": task.status,
        "message": task.message,
        "updated": task.updated.isoformat(),
        "items": task.items,
    }


################################################################################
# Task Status
#
@router.get("/{task_id}")
async def get_task(response: fastapi.Response, task_id: str):
    response.headers["Cache-Control"] = "no-cache"
    try:
        return _get_task_info(task_id)
    except KeyError:
        raise fastapi.HTTPException(status_code=404, detail="Task not found.")


@router.websocket("/{task_id}")
async def get_task_ws(websocket: fastapi.WebSocket, task_id: str):
    """Websocket Connection to request a task's status.

    Sends the updated Status every 1 second.
    Stops after 100 iterations

    """
    await websocket.accept()

    # max number of iterations before giving up
    max_iterations = 100
    n_err = 0

    for _ in range(max_iterations):
        try:
            info = _get_task_info(task_id)
        except KeyError:
            await websocket.send_json({"status": "not found"})
            n_err += 1
            await asyncio.sleep(1 + n_err)  # auto-throttle based on number of errros to
        else:
            await websocket.send_json(info)
            await asyncio.sleep(1)

    else:
        await websocket.send_json({"status": "timeout"})
