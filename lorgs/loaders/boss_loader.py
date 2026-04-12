"""Loaders for Actor (Player / Boss) data from WarcraftLogs."""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from .actor_loader import ActorLoader


if typing.TYPE_CHECKING:
    from lorgs.models.warcraftlogs_boss import Boss


class BossLoader(ActorLoader):
    """Loader for Boss actors."""

    actor: Boss

    def set_source_id_from_events(self, *_, **__) -> None:
        """No-op for Boss actors.

        In case of council fights there could be multiple source_ids for the same boss.
        """
        return
