"""Midnight Season 2."""
# ruff: ignore[unsorted-imports] We like them sorted by expansion

# IMPORT LOCAL LIBRARIES
from lorgs.data.expansions.midnight.consumables import (
    LIGHTFUSED_MANA_POTION,
    LIGHTS_POTENTIAL,
    LIQUID_LUSTER,
    POTION_OF_RECKLESSNESS,
    SILVERMOON_HEALTH_POTION,
)
from lorgs.models.season import Season

# Dungeons
from lorgs.data.expansions.battle_for_azeroth.dungeons import KINGS_REST
from lorgs.data.expansions.battle_for_azeroth.dungeons import TEMPLE_OF_SETHRALISS
from lorgs.data.expansions.dragonflight.dungeons import RUBY_LIFE_POOLS
from lorgs.data.expansions.midnight.dungeons import ALTAR_OF_FANGS
from lorgs.data.expansions.midnight.dungeons import DEN_OF_NALORAKK
from lorgs.data.expansions.midnight.dungeons import MURDER_ROW
from lorgs.data.expansions.midnight.dungeons import THE_BLINDING_VALE
from lorgs.data.expansions.midnight.dungeons import VOIDSCAR_ARENA

# Raids
from lorgs.data.expansions.midnight.raids import THE_VENOMOUS_ABYSS
from lorgs.data.expansions.midnight.raids import THE_TIDEBOUND_GROTTO
from lorgs.data.expansions.midnight.raids import THE_UNBINDING_OF_KITHIX


MIDNIGHT_SEASON2 = Season(
    name="Midnight Season 2",
    slug="midnight_s2",
    ilvl=344,
    consumables=[SILVERMOON_HEALTH_POTION, LIGHTFUSED_MANA_POTION, LIGHTS_POTENTIAL, POTION_OF_RECKLESSNESS, LIQUID_LUSTER],
    raids=[
        THE_VENOMOUS_ABYSS,
        THE_TIDEBOUND_GROTTO,
        THE_UNBINDING_OF_KITHIX,
    ],
    dungeons=[
        ALTAR_OF_FANGS,
        MURDER_ROW,
        DEN_OF_NALORAKK,
        THE_BLINDING_VALE,
        VOIDSCAR_ARENA,
        KINGS_REST,
        TEMPLE_OF_SETHRALISS,
        RUBY_LIFE_POOLS,
    ],
)
