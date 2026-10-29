"""Selectors (spec, boss, difficulty, metric) turn into the Spec Rankings they name."""

import pytest

from lorgs.models import selectors
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.game_data import GameData
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.raid_zone import AUTO_DIFFICULTY, RaidZone
from lorgs.models.season import Season
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_role import WowRole
from lorgs.models.wow_spec import WowSpec


HEAL = WowRole(id=90201, code="selector-heal", name="Selector Healer", metric="hps", metrics=["hps", "dps"])
DPS = WowRole(id=90202, code="selector-dps", name="Selector Damage", metrics=["dps", "bossdps"])
ITEMS = WowRole(id=90203, code="selector-item", name="Selector Items", playable=False)

PLAYER_CLASS = WowClass(id=90201, name="Selector Class")
ITEM_CLASS = WowClass(id=90202, name="Selector Other")

HEALER = WowSpec(role=HEAL, wow_class=PLAYER_CLASS, name="Healer")
DAMAGE = WowSpec(role=DPS, wow_class=PLAYER_CLASS, name="Damage")
TRINKETS = WowSpec(role=ITEMS, wow_class=ITEM_CLASS, name="Trinkets")

FIXED_BOSS = RaidBoss(id=90201, name="Selector Fixed Boss")
FLEXIBLE_BOSS = RaidBoss(id=90202, name="Selector Flexible Boss")


@pytest.fixture(name="game_data")
def fixture_game_data() -> GameData:
    fixed = RaidZone(id=90201, name="Selector Fixed Zone", difficulty=RaidDifficulty.HEROIC, bosses=[FIXED_BOSS])
    flexible = RaidZone(id=90202, name="Selector Flexible Zone", bosses=[FLEXIBLE_BOSS])
    season = Season(name="Selector Season", ilvl=1, raids=[fixed, flexible])
    return GameData(
        roles=[HEAL, DPS, ITEMS],
        classes=[PLAYER_CLASS, ITEM_CLASS],
        season=season,
        difficulties=(RaidDifficulty.HEROIC, RaidDifficulty.MYTHIC),
    )


def test_all_specs_skips_pseudo_specs(game_data: GameData) -> None:
    assert set(selectors.select_specs(game_data, "all")) == {HEALER, DAMAGE}
    assert selectors.select_specs(game_data, TRINKETS.full_name_slug) == [TRINKETS]
    assert selectors.select_specs(game_data, "unknown-spec") == []


def test_all_bosses_are_the_current_seasons(game_data: GameData) -> None:
    assert selectors.select_bosses(game_data, "all") == [FIXED_BOSS, FLEXIBLE_BOSS]
    assert selectors.select_bosses(game_data, "unknown-boss") == []


def test_difficulties(game_data: GameData) -> None:
    assert selectors.select_difficulties(game_data, FIXED_BOSS.full_name_slug, "all") == ["heroic"]
    assert selectors.select_difficulties(game_data, FLEXIBLE_BOSS.full_name_slug, "all") == ["heroic", "mythic"]
    assert selectors.select_difficulties(game_data, FLEXIBLE_BOSS.full_name_slug, AUTO_DIFFICULTY) == ["mythic"]
    assert selectors.select_difficulties(game_data, FLEXIBLE_BOSS.full_name_slug, "heroic") == ["heroic"]


def test_metrics_default_to_the_role() -> None:
    assert selectors.default_metric(HEALER) == "hps"
    assert selectors.default_metric(None) == "dps"
    assert selectors.select_metrics(HEALER, "") == ["hps"]
    assert selectors.select_metrics(HEALER, "dps") == ["dps"]
    assert selectors.select_metrics(DAMAGE, "all") == ["dps", "bossdps"]


def test_expand_selectors(game_data: GameData) -> None:
    keys = selectors.expand_selectors(
        game_data,
        selectors.select_specs(game_data, "all"),
        selectors.select_bosses(game_data, "all"),
        difficulty="all",
        metric="all",
    )

    assert {(key.spec, key.boss, key.difficulty, key.metric) for key in keys} == {
        (spec, boss, difficulty, metric)
        for spec in (HEALER, DAMAGE)
        for boss, difficulties in ((FIXED_BOSS, ["heroic"]), (FLEXIBLE_BOSS, ["heroic", "mythic"]))
        for difficulty in difficulties
        for metric in spec.role.metrics
    }
    assert len(keys) == 2 * 3 * 2
