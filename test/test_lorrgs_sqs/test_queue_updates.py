"""Seams: `scripts/queue_updates.py` queues for the Game Version it is given."""

from __future__ import annotations

import importlib.util
import pathlib
import sys
from unittest import mock

import pytest

from lorgs.data import FOREVER, MISTS


@pytest.fixture(name="queue_updates")
def fixture_queue_updates():
    path = pathlib.Path("scripts/queue_updates.py")
    spec = importlib.util.spec_from_file_location("queue_updates_script", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_tasks_and_payloads_carry_the_game_version(queue_updates) -> None:
    parser = queue_updates.build_parser()
    args = parser.parse_args(["--game-version", "mists", "--boss", "the-stone-guard", "--spec", "mage-fire"])

    game_version = queue_updates.GAME_VERSIONS[args.game_version]
    bosses = queue_updates.select_bosses(parser, args, game_version.data)
    specs = queue_updates.select_specs(parser, args, game_version.data)
    (task,) = queue_updates.build_tasks(game_version, specs, bosses, args.difficulty, args.metric)

    assert task.game_version is MISTS
    assert task.difficulty == "heroic"
    with mock.patch.object(queue_updates.sqs, "send_message_batch") as send_message_batch:
        queue_updates.load_remote([task])
    (payload,) = send_message_batch.call_args.args[0]
    assert payload.game_version == "mists"


def test_selection_is_limited_to_the_given_game_version(queue_updates) -> None:
    parser = queue_updates.build_parser()
    args = parser.parse_args(["--game-version", "forever"])

    assert {boss.full_name_slug for boss in queue_updates.select_bosses(parser, args, FOREVER.data)} == {
        boss.full_name_slug for boss in FOREVER.data.bosses
    }
    assert {spec.full_name_slug for spec in queue_updates.select_specs(parser, args, FOREVER.data)} == {
        spec.full_name_slug for spec in FOREVER.data.specs
    }

    mists_args = parser.parse_args(["--game-version", "mists", "--boss", "the-stone-guard"])
    with pytest.raises(SystemExit):
        queue_updates.select_bosses(parser, mists_args, FOREVER.data)
