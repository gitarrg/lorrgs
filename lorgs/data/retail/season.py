"""Defines which Raid/Dungeon the current Season includes."""

from lorgs.data.retail.seasons import MIDNIGHT_SEASON2


CURRENT_SEASON = MIDNIGHT_SEASON2
CURRENT_SEASON.activate()


__all__ = [
    "CURRENT_SEASON",
]
