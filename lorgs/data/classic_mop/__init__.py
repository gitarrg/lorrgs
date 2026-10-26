"""Game data of the WoW Classic: Mists of Pandaria Game Version.

A skeleton: no Classes, Specs, Raids or Dungeons are registered yet.
The `lorgs.data` package loads this package when Classic MoP is the active Game Version.
"""

from lorgs.data.classic_mop.season import CURRENT_SEASON


__all__ = [
    "CURRENT_SEASON",
]
