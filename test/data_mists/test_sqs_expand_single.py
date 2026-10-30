"""A payload whose keyword expands to a single value runs with that value."""

import asyncio
import json
from unittest import mock

from lorgs.data import MISTS
from lorrgs_sqs import handler


def test_difficulty_all_in_a_single_difficulty_zone_runs_resolved() -> None:
    spec = MISTS.data.specs[0]
    boss = MISTS.data.bosses[0]
    payload = {
        "task": "load_spec_rankings",
        "game_version": MISTS.name,
        "spec_slug": spec.full_name_slug,
        "boss_slug": boss.full_name_slug,
        "difficulty": "all",
        "metric": "dps",
    }
    task_handler = mock.AsyncMock()

    with (
        mock.patch.dict(handler.TASK_HANDLERS, {"load_spec_rankings": task_handler}),
        mock.patch.object(handler, "submit_messages") as submit,
    ):
        asyncio.run(handler.process_message({"body": json.dumps(payload)}))

    submit.assert_not_called()
    body = json.loads(task_handler.call_args.args[0]["body"])
    assert body["difficulty"] == MISTS.data.resolve_difficulty(boss.full_name_slug, "auto")
