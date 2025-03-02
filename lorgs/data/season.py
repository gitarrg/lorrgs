"""Defines which Raid/Dungeon the current Season includes."""

from lorgs.data.expansions.the_war_within.seasons.tww_s1 import TWW_SEASON1
from lorgs.data.expansions.the_war_within.seasons.tww_s2 import TWW_SEASON2


ALL_SEASONS = [
    TWW_SEASON1,
    TWW_SEASON2,
]


CURRENT_SEASON = TWW_SEASON2
CURRENT_SEASON.activate()


__all__ = [
    "ALL_SEASONS",
    "CURRENT_SEASON",
]
