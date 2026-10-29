"""Actor-load pipeline runs Actor Type cast processing."""

import asyncio
import datetime
import logging

import pytest

import lorgs.data.retail.classes.demonhunter  # noqa: F401  # registers Devourer and its load handler
import lorgs.data.retail.classes.druid  # noqa: F401  # registers Restoration Druid
import lorgs.data.retail.classes.evoker  # noqa: F401  # registers Preservation and its load handlers
import lorgs.data.retail.classes.hunter  # noqa: F401  # registers Marksmanship and its load handler
import lorgs.data.retail.classes.shaman  # noqa: F401  # registers Restoration Shaman and its load handler
from lorgs.data.retail import GAME_DATA, HEAL
from lorgs.loaders.actor_loader import ActorLoader
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.game_data import GameData
from lorgs.models.season import Season
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


def _aura(timestamp: int, spell_id: int, event_type: str, source_id: int = 10) -> dict[str, int | str]:
    return {
        "timestamp": timestamp,
        "type": event_type,
        "sourceID": source_id,
        "targetID": source_id,
        "abilityGameID": spell_id,
    }


def _load(spec_slug: str, events: dict, game_data: GameData | None = None) -> Player:
    player = Player(source_id=10, spec_slug=spec_slug, name="Healer")
    ActorLoader(player, game_data or GAME_DATA).process_query_result(events)
    return player


def _process(spec_slug: str, events: dict, game_data: GameData | None = None) -> list[tuple[int, int, int]]:
    return [(cast.spell_id, cast.timestamp, cast.counter) for cast in _load(spec_slug, events, game_data).casts]


def _with_duration(spec_slug: str, events: dict) -> list[tuple[int, int, int | None, int]]:
    return [(cast.spell_id, cast.timestamp, cast.duration, cast.counter) for cast in _load(spec_slug, events).casts]


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
    chain_role = WowRole(id=59003, name="Chain Role", code="chain-role")

    class ChainSpec(WowSpec):
        id: int = 59002
        index: int = 1
        name: str = "Chain Spec"
        role: WowRole = chain_role
        wow_class: WowClass = chain_class

        def process_casts(self, casts: list[Cast]) -> list[Cast]:
            class_already_ran = any(cast.spell_id == CLASS_MARK for cast in casts)
            mark = SPEC_AFTER_CLASS if class_already_ran else SPEC_BEFORE_CLASS
            return [*casts, Cast(spell_id=mark, timestamp=2)]

    spec = ChainSpec()
    season = Season(name="Chain Season", ilvl=1)
    game_data = GameData(roles=[spec.role], classes=[chain_class], seasons=[season], current_season=season, difficulties=(RaidDifficulty.HEROIC,))
    events = _events(_cast(1_000, 50))

    assert _process(spec.full_name_slug, events, game_data) == [
        (CLASS_MARK, 1, 1),
        (SPEC_AFTER_CLASS, 2, 1),
        (50, 1_000, 1),
    ]


VOID_METAMORPHOSIS = 1217607
DROP_VOID_META = 267134


def test_void_metamorphosis_gains_a_drop_cast_at_its_end_in_time_order(capsys: pytest.CaptureFixture[str]) -> None:
    """Each Void Metamorphosis yields a Drop Void Meta Cast at its end, numbered in time order."""
    events = _events(
        _aura(0, VOID_METAMORPHOSIS, "applybuff"),
        _cast(5_000, 1246167),
        _aura(10_000, VOID_METAMORPHOSIS, "removebuff"),
        _aura(20_000, VOID_METAMORPHOSIS, "applybuff"),
        _aura(28_000, VOID_METAMORPHOSIS, "removebuff"),
    )

    assert _process("demonhunter-devourer", events) == [
        (VOID_METAMORPHOSIS, 0, 1),
        (1246167, 5_000, 1),
        (DROP_VOID_META, 10_000, 1),
        (VOID_METAMORPHOSIS, 20_000, 2),
        (DROP_VOID_META, 28_000, 2),
    ]
    assert capsys.readouterr().out == ""


def test_actor_load_does_not_add_drop_void_meta_casts() -> None:
    """actor.load does not add Drop Void Meta Casts."""
    player = Player(source_id=10, spec_slug="demonhunter-devourer", name="Devourer")
    player.casts = [Cast(spell_id=VOID_METAMORPHOSIS, timestamp=0, duration=10_000)]

    player.event_actor_load.send(player, status="success")

    assert [(cast.spell_id, cast.timestamp) for cast in player.casts] == [
        (VOID_METAMORPHOSIS, 0),
    ]


ASCENDANCE = 114052
DEEPLY_ROOTED_ELEMENTS = 378270


def test_short_ascendance_is_a_proc_and_full_ascendance_keeps_its_own_counter() -> None:
    """A short Ascendance buff is Deeply Rooted Elements; a full one stays Ascendance, counted apart."""
    events = _events(
        _aura(0, ASCENDANCE, "applybuff"),
        _aura(6_000, ASCENDANCE, "removebuff"),
        _aura(20_000, ASCENDANCE, "applybuff"),
        _aura(50_000, ASCENDANCE, "removebuff"),
    )

    assert _process("shaman-restoration", events) == [
        (DEEPLY_ROOTED_ELEMENTS, 0, 1),
        (ASCENDANCE, 20_000, 1),
    ]


def test_actor_load_does_not_split_restoration_shaman_ascendance_procs() -> None:
    """actor.load does not rewrite a short Ascendance buff."""
    player = Player(source_id=10, spec_slug="shaman-restoration", name="Resto")
    player.casts = [Cast(spell_id=ASCENDANCE, timestamp=0, duration=6_000, event_type="applybuff")]

    player.event_actor_load.send(player, status="success")

    assert [(cast.spell_id, cast.timestamp) for cast in player.casts] == [
        (ASCENDANCE, 0),
    ]


EXPLOSIVE_SHOT = 212431
VOLLEY = 260243


def test_explosive_shot_recasts_within_ten_seconds_are_dropped_and_renumbered() -> None:
    """Explosive Shots within 10s collapse to the first; shots more than 10s apart both remain."""
    events = _events(
        _cast(0, EXPLOSIVE_SHOT),
        _cast(5_000, EXPLOSIVE_SHOT),
        _cast(8_000, VOLLEY),
        _cast(16_000, EXPLOSIVE_SHOT),
    )

    assert _process("hunter-marksmanship", events) == [
        (EXPLOSIVE_SHOT, 0, 1),
        (VOLLEY, 8_000, 1),
        (EXPLOSIVE_SHOT, 16_000, 2),
    ]


def test_actor_load_does_not_drop_marksmanship_explosive_shot_recasts() -> None:
    """actor.load does not drop Explosive Shot recasts."""
    player = Player(source_id=10, spec_slug="hunter-marksmanship", name="Hunter")
    player.casts = [
        Cast(spell_id=EXPLOSIVE_SHOT, timestamp=0),
        Cast(spell_id=EXPLOSIVE_SHOT, timestamp=5_000),
    ]

    player.event_actor_load.send(player, status="success")

    assert [(cast.spell_id, cast.timestamp) for cast in player.casts] == [
        (EXPLOSIVE_SHOT, 0),
        (EXPLOSIVE_SHOT, 5_000),
    ]


STASIS = 370537
STASIS_POP = 370564
DREAM_BREATH = 355936


def test_stasis_charge_keeps_the_duration_until_release() -> None:
    """A Stasis charge followed by its release carries the time until that release."""
    events = _events(
        _cast(5_000, STASIS),
        _cast(25_000, STASIS_POP),
    )

    assert _with_duration("evoker-preservation", events) == [
        (STASIS, 5_000, 20_000, 1),
        (STASIS_POP, 25_000, None, 1),
    ]


def test_stasis_charged_before_the_pull_starts_a_full_duration_earlier() -> None:
    """A lone release stays put and gains a charge one full Stasis duration earlier."""
    events = _events(_cast(26_000, STASIS_POP))

    assert _with_duration("evoker-preservation", events) == [
        (STASIS, -4_000, 30_000, 1),
        (STASIS_POP, 26_000, None, 1),
    ]


def test_dream_breath_released_by_stasis_is_dropped_and_a_later_one_is_numbered_alone() -> None:
    """Dream Breath within about a second of Stasis Pop is removed; a later one stays."""
    events = _events(
        _cast(0, STASIS),
        _cast(10_000, STASIS_POP),
        _cast(10_500, DREAM_BREATH),
        _cast(12_000, DREAM_BREATH),
    )

    assert _process("evoker-preservation", events) == [
        (STASIS, 0, 1),
        (STASIS_POP, 10_000, 1),
        (DREAM_BREATH, 12_000, 1),
    ]


def test_actor_load_does_not_apply_preservation_stasis_fixes() -> None:
    """actor.load does not change Stasis durations or drop spells Stasis released."""
    player = Player(source_id=10, spec_slug="evoker-preservation", name="Evoker")
    player.casts = [
        Cast(spell_id=STASIS, timestamp=5_000),
        Cast(spell_id=STASIS_POP, timestamp=25_000),
        Cast(spell_id=DREAM_BREATH, timestamp=25_500),
    ]

    player.event_actor_load.send(player, status="success")

    assert [(cast.spell_id, cast.timestamp, cast.duration) for cast in player.casts] == [
        (STASIS, 5_000, None),
        (STASIS_POP, 25_000, None),
        (DREAM_BREATH, 25_500, None),
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
