"""The `auto` difficulty resolves to the one difficulty a RaidZone ranks."""

import pytest

from lorgs.game_version import ACTIVE
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.game_data import GameData
from lorgs.models.raid_zone import AUTO_DIFFICULTY, RaidZone
from lorgs.models.season import Season


@pytest.fixture(name="zones")
def fixture_zones() -> tuple[RaidZone, RaidZone]:
    fixed = RaidZone(
        id=9001,
        name="Fixed Zone",
        difficulty=RaidDifficulty.HEROIC,
        bosses=[RaidBoss(id=90011, name="Fixed Boss")],
    )
    flexible = RaidZone(id=9002, name="Flexible Zone", bosses=[RaidBoss(id=90021, name="Flexible Boss")])
    return fixed, flexible


@pytest.fixture(name="game_data")
def fixture_game_data(zones: tuple[RaidZone, RaidZone]) -> GameData:
    season = Season(name="Fixture Season", ilvl=1, raids=list(zones))
    return GameData(roles=[], classes=[], seasons=[season], current_season=season)


def test_auto_resolves_to_the_zones_difficulty(zones: tuple[RaidZone, RaidZone], game_data: GameData) -> None:
    fixed, _ = zones
    assert game_data.resolve_difficulty(fixed.bosses[0].full_name_slug, AUTO_DIFFICULTY) == "heroic"


def test_auto_falls_back_to_the_game_version_default(zones: tuple[RaidZone, RaidZone], game_data: GameData) -> None:
    _, flexible = zones
    assert game_data.resolve_difficulty(flexible.bosses[0].full_name_slug, AUTO_DIFFICULTY) == ACTIVE.default_difficulty_name
    assert game_data.resolve_difficulty("unknown-boss", AUTO_DIFFICULTY) == ACTIVE.default_difficulty_name


def test_explicit_difficulty_is_unchanged(zones: tuple[RaidZone, RaidZone], game_data: GameData) -> None:
    fixed, _ = zones
    assert game_data.resolve_difficulty(fixed.bosses[0].full_name_slug, "mythic") == "mythic"


def test_difficulties_for_boss(zones: tuple[RaidZone, RaidZone], game_data: GameData) -> None:
    fixed, flexible = zones
    assert game_data.difficulties_for_boss(fixed.bosses[0].full_name_slug) == ["heroic"]
    assert game_data.difficulties_for_boss(flexible.bosses[0].full_name_slug) == list(ACTIVE.difficulty_names)


def test_as_dict_exposes_the_difficulty(zones: tuple[RaidZone, RaidZone]) -> None:
    fixed, flexible = zones
    assert fixed.as_dict()["difficulty"] == "heroic"
    assert flexible.as_dict()["difficulty"] is None
