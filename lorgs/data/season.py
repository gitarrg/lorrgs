"""Defines which Raid/Dungeon the current Season includes."""

from lorgs.data.expansions.midnight.seasons.midnight_s1 import MIDNIGHT_SEASON1


CURRENT_SEASON = MIDNIGHT_SEASON1
CURRENT_SEASON.activate()


__all__ = [
    "ALL_SEASONS",
    "CURRENT_SEASON",
]
