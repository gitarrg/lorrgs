"""War Within Season 2."""

# IMPORT LOCAL LIBRARIES
# Dungeons
from lorgs.data.expansions.battle_for_azeroth import SIEGE_OF_BORALUS
from lorgs.data.expansions.cataclysm import GRIM_BATOL
from lorgs.data.expansions.shadowlands import MISTS_OF_TIRNA_SCITHE, NECROTIC_WAKE

# Raids
from lorgs.data.expansions.the_war_within import ARA_KARA, CITY_OF_THREADS, DAWNBREAKER, NERUBAR_PALACE, STONEVAULT
from lorgs.data.expansions.the_war_within.consumables import (
    Algari_Healing_Potion,
    Algari_Mana_Potion,
    Tempered_Potion,
)
from lorgs.models.season import Season


TWW_SEASON1 = Season(
    name="TWW Season 1",
    slug="tww_s1",
    ilvl=639,
    consumables=[Algari_Healing_Potion, Tempered_Potion, Algari_Mana_Potion],
    raids=[
        NERUBAR_PALACE,
    ],
    dungeons=[
        ARA_KARA,
        CITY_OF_THREADS,
        DAWNBREAKER,
        STONEVAULT,
        MISTS_OF_TIRNA_SCITHE,
        NECROTIC_WAKE,
        SIEGE_OF_BORALUS,
        GRIM_BATOL,
    ],
)
