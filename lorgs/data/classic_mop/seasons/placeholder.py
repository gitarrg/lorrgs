"""Placeholder Season, so the Classic MoP deployment has a current Season while it has no Raids."""

# IMPORT LOCAL LIBRARIES
from lorgs.models.season import Season


CLASSIC_MOP_PLACEHOLDER_SEASON = Season(
    name="WoW Classic: Mists of Pandaria",
    slug="classic_mop",
    ilvl=0,
    raids=[],
    dungeons=[],
)
