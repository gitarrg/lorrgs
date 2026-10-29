# IMPORT LOCAL LIBRARIES
from lorgs.models import base
from lorgs.models.wow_trinket import WowTrinket


class Dungeon(base.StaticModel):
    """A Dungeon in the Game."""

    name: str
    """Full Name."""

    trinkets: list[WowTrinket] = []
    """List of (relevant) Trinkets that drop from Bosses inside the Dungeon."""
