"""Mists of Pandaria Classic phases, one Season each."""

# IMPORT LOCAL LIBRARIES
from lorgs.data.expansions.mists_of_pandaria import (
    HEART_OF_FEAR,
    MOGUSHAN_VAULTS,
    SIEGE_OF_ORGRIMMAR,
    TERRACE_OF_ENDLESS_SPRING,
    THRONE_OF_THUNDER,
)
from lorgs.models.season import Season


# Phase 1, July 21, 2025. Modules are not written yet.
DUNGEONS = [
    # TEMPLE_OF_THE_JADE_SERPENT,
    # STORMSTOUT_BREWERY,
    # MOGUSHAN_PALACE,
    # SHADO_PAN_MONASTERY,
    # GATE_OF_THE_SETTING_SUN,
    # SIEGE_OF_NIUZAO_TEMPLE,
    # SCARLET_HALLS,
    # SCARLET_MONASTERY,
    # SCHOLMANCE,
]


# July 21, 2025. Dungeons, then the Tier 14 raids. Sha of Anger and Galleon are world bosses.
MISTS_PHASE1 = Season(
    name="Mists of Pandaria Phase 1",
    slug="mists_phase1",
    ilvl=509,
    raids=[
        MOGUSHAN_VAULTS,  # July 31, 2025
        HEART_OF_FEAR,  # August 21, 2025
        TERRACE_OF_ENDLESS_SPRING,  # September 4, 2025
    ],
    dungeons=DUNGEONS,
)

# September 23, 2025. Landfall, the upgrade system, Brawler's Guild. No new raids or dungeons.
MISTS_PHASE2 = Season(
    name="Mists of Pandaria Phase 2",
    slug="mists_phase2",
    ilvl=509,
    raids=MISTS_PHASE1.raids,
    dungeons=DUNGEONS,
)

# December 9, 2025. Heroic 535, Thunderforged 542.
MISTS_PHASE3 = Season(
    name="Mists of Pandaria Phase 3",
    slug="mists_phase3",
    ilvl=535,
    raids=[
        *MISTS_PHASE1.raids,
        THRONE_OF_THUNDER,  # December 9, 2025
    ],
    dungeons=DUNGEONS,
)

# March 31, 2026. Heroic scenarios. No new raids or dungeons.
MISTS_PHASE4 = Season(
    name="Mists of Pandaria Phase 4",
    slug="mists_phase4",
    ilvl=535,
    raids=MISTS_PHASE3.raids,
    dungeons=DUNGEONS,
)

# June 2, 2026. Heroic 566, Warforged 572, heirloom weapons 582.
MISTS_PHASE5 = Season(
    name="Mists of Pandaria Phase 5",
    slug="mists_phase5",
    ilvl=566,
    raids=[
        *MISTS_PHASE3.raids,
        SIEGE_OF_ORGRIMMAR,  # June 2, 2026
    ],
    dungeons=DUNGEONS,
)
