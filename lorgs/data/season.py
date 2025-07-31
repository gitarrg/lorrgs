"""Defines which Raid/Dungeon the current Season includes."""

from lorgs.data.expansions.the_war_within.seasons.tww_s1 import TWW_SEASON1
from lorgs.data.expansions.the_war_within.seasons.tww_s2 import TWW_SEASON2
from lorgs.data.expansions.the_war_within.seasons.tww_s3 import TWW_SEASON3


ALL_SEASONS = [
    TWW_SEASON1,
    TWW_SEASON2,
    TWW_SEASON3,
]


CURRENT_SEASON = TWW_SEASON3
CURRENT_SEASON.activate()


__all__ = [
    "ALL_SEASONS",
    "CURRENT_SEASON",
]
