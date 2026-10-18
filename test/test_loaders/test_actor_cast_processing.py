"""Actor-load pipeline runs Actor Type cast processing."""

import asyncio
import datetime
import logging

import pytest

import lorgs.data.classes.druid  # noqa: F401  # registers Restoration Druid
from lorgs.data.roles import HEAL
from lorgs.loaders.actor_loader import ActorLoader
from lorgs.models.warcraftlogs_actor import BaseActor
from lorgs.models.warcraftlogs_cast import Cast
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_player import Player
from lorgs.models.warcraftlogs_report import Report
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_role import WowRole
from lorgs.models.wow_spec import WowSpec
from test.helpers import wrap_data


TREE_OF_LIFE = 33891
TRANQUILITY = 740


def _events(*rows: dict[str, int | str]) -> dict:
    return wrap_data(list(rows), "report", "events", "data")


def _cast(timestamp: int, spell_id: int, source_id: int = 10) -> dict[str, int | str]:
    return {
        "timestamp": timestamp,
        "type": "cast",
        "sourceID": source_id,
        "abilityGameID": spell_id,
    }


def _process(spec_slug: str, events: dict) -> list[tuple[int, int, int]]:
    player = Player(source_id=10, spec_slug=spec_slug, name="Healer")
    ActorLoader(player).process_query_result(events)
    return [(cast.spell_id, cast.timestamp, cast.counter) for cast in player.casts]


def test_tree_of_life_recast_within_cooldown_is_dropped_and_remaining_casts_are_numbered() -> None:
    """Two Tree of Life casts inside its cooldown leave the first, numbered 1..n."""
    events = _events(
        _cast(0, TREE_OF_LIFE),
        _cast(30_000, TREE_OF_LIFE),
        _cast(60_000, TRANQUILITY),
        _cast(180_000, TREE_OF_LIFE),
    )

    assert _process("druid-restoration", events) == [
        (TREE_OF_LIFE, 0, 1),
        (TRANQUILITY, 60_000, 1),
        (TREE_OF_LIFE, 180_000, 2),
    ]


def test_non_druid_keeps_tree_of_life_casts_inside_the_cooldown() -> None:
    """The Tree of Life fix does not apply to a non-Druid actor."""
    events = _events(
        _cast(0, TREE_OF_LIFE),
        _cast(30_000, TREE_OF_LIFE),
    )

    assert _process("priest-holy", events) == [
        (TREE_OF_LIFE, 0, 1),
        (TREE_OF_LIFE, 30_000, 2),
    ]


CLASS_MARK = 9001
SPEC_AFTER_CLASS = 9002
SPEC_BEFORE_CLASS = 9003


def test_class_process_casts_runs_before_spec_process_casts() -> None:
    """A class-level and a spec-level process_casts both run, class first."""

    class ChainClass(WowClass):
        id: int = 59001
        name: str = "Chain Class"

        def process_casts(self, casts: list[Cast]) -> list[Cast]:
            return [*casts, Cast(spell_id=CLASS_MARK, timestamp=1)]

    chain_class = ChainClass()

    class ChainSpec(WowSpec):
        id: int = 59002
        index: int = 1
        name: str = "Chain Spec"
        role: WowRole = HEAL
        wow_class: WowClass = chain_class

        def process_casts(self, casts: list[Cast]) -> list[Cast]:
            class_already_ran = any(cast.spell_id == CLASS_MARK for cast in casts)
            mark = SPEC_AFTER_CLASS if class_already_ran else SPEC_BEFORE_CLASS
            return [*casts, Cast(spell_id=mark, timestamp=2)]

    spec = ChainSpec()
    events = _events(_cast(1_000, 50))

    assert _process(spec.full_name_slug, events) == [
        (CLASS_MARK, 1, 1),
        (SPEC_AFTER_CLASS, 2, 1),
        (50, 1_000, 1),
    ]


def test_actor_load_does_not_drop_restoration_druid_tree_of_life_recasts() -> None:
    """actor.load does not mutate a Restoration Druid's Tree of Life casts."""
    player = Player(source_id=10, spec_slug="druid-restoration", name="Healer")
    player.casts = [
        Cast(spell_id=TREE_OF_LIFE, timestamp=0),
        Cast(spell_id=TREE_OF_LIFE, timestamp=30_000),
    ]

    player.event_actor_load.send(player, status="success")

    assert [(cast.spell_id, cast.timestamp) for cast in player.casts] == [
        (TREE_OF_LIFE, 0),
        (TREE_OF_LIFE, 30_000),
    ]
