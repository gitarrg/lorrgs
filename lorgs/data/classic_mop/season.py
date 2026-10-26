"""Defines which Raid/Dungeon the current Season includes."""

from lorgs.data.classic_mop.seasons import CLASSIC_MOP_PLACEHOLDER_SEASON


CURRENT_SEASON = CLASSIC_MOP_PLACEHOLDER_SEASON
CURRENT_SEASON.activate()


__all__ = [
    "CURRENT_SEASON",
]
