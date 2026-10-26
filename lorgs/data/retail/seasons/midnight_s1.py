"""Midnight Season 1."""

# IMPORT LOCAL LIBRARIES
# Dungeons
from lorgs.data.expansions.cataclysm.dungeons import SKYREACH
from lorgs.data.expansions.dragonflight.dungeons import ALGETHAR_ACADEMY
from lorgs.data.expansions.legion.dungeons import SEAT_OF_THE_TRIUMVIRATE
from lorgs.data.expansions.midnight.dungeons import (
    MAGISTERS_TERRACE,
    MAISARA_CAVERNS,
    NEXUS_POINT_XENAS,
    WINDRUNNER_SPIRE,
)

# Raids
from lorgs.data.expansions.midnight.raids import DREAMRIFT, MARCH_ON_QUALDANAS, SPOREFALL, VOIDSPIRE
from lorgs.data.expansions.wrath_of_the_lich_king.dungeons import PIT_OF_SARON
from lorgs.models.season import Season


MIDNIGHT_SEASON1 = Season(
    name="Midnight Season 1",
    slug="midnight_s1",
    ilvl=289,
    raids=[
        VOIDSPIRE,
        DREAMRIFT,
        MARCH_ON_QUALDANAS,
        SPOREFALL,
    ],
    dungeons=[
        ALGETHAR_ACADEMY,
        MAGISTERS_TERRACE,
        MAISARA_CAVERNS,
        NEXUS_POINT_XENAS,
        PIT_OF_SARON,
        SEAT_OF_THE_TRIUMVIRATE,
        SKYREACH,
        WINDRUNNER_SPIRE,
    ],
)
