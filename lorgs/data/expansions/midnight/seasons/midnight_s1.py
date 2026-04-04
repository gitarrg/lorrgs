"""Midnight Season 1."""

# IMPORT LOCAL LIBRARIES
from lorgs.models.season import Season

# Dungeons
from lorgs.data.expansions.cataclysm.dungeons import SKYREACH
from lorgs.data.expansions.dragonflight.dungeons import ALGETHAR_ACADEMY
from lorgs.data.expansions.legion.dungeons import SEAT_OF_THE_TRIUMVIRATE
from lorgs.data.expansions.midnight.dungeons import MAGISTERS_TERRACE
from lorgs.data.expansions.midnight.dungeons import MAISARA_CAVERNS
from lorgs.data.expansions.midnight.dungeons import NEXUS_POINT_XENAS
from lorgs.data.expansions.midnight.dungeons import WINDRUNNER_SPIRE
from lorgs.data.expansions.wrath_of_the_lich_king.dungeons import PIT_OF_SARON

# Raids
from lorgs.data.expansions.midnight.raids import VOIDSPIRE
from lorgs.data.expansions.midnight.raids import DREAMRIFT
from lorgs.data.expansions.midnight.raids import MARCH_ON_QUALDANAS


MIDNIGHT_SEASON1 = Season(
    name="Midnight Season 1",
    slug="midnight_s1",
    ilvl=289,
    raids=[
        VOIDSPIRE,
        DREAMRIFT,
        MARCH_ON_QUALDANAS,
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
