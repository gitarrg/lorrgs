"""Defines which Raid/Dungeon the current Season includes."""

from lorgs.data.mists.seasons import MISTS_SEASON


CURRENT_SEASON = MISTS_SEASON
CURRENT_SEASON.activate()


__all__ = [
    "CURRENT_SEASON",
]
