"""Defines which Raid/Dungeon the current Season includes."""

from lorgs.data.forever.seasons import FOREVER_PLACEHOLDER_SEASON


CURRENT_SEASON = FOREVER_PLACEHOLDER_SEASON
CURRENT_SEASON.activate()


__all__ = [
    "CURRENT_SEASON",
]
