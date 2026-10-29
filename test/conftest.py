"""Fixtures shared by the generic tests.

Generic tests never rely on a Game Version's real game data (that is what `data_retail/` and `data_forever/` are for):
they build what they need from these fixtures.
"""

import pytest

from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.game_data import GameData
from lorgs.models.season import Season
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_role import WowRole
from lorgs.models.wow_spec import WowSpec


@pytest.fixture
def spec() -> WowSpec:
    """A Spec that is registered for the length of the test."""
    role = WowRole(id=90101, name="Fixture Role", code="fixture-role")
    wow_class = WowClass(id=90101, name="Fixture Class")
    return WowSpec(name="Fixture Spec", role=role, wow_class=wow_class)


@pytest.fixture
def game_data(spec: WowSpec) -> GameData:
    """Game Data holding only the `spec` fixture."""
    season = Season(name="Fixture Season", ilvl=1)
    return GameData(roles=[spec.role], classes=[spec.wow_class], season=season, difficulties=(RaidDifficulty.HEROIC,))
