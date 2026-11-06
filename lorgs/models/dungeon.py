# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base
from lorgs.models.wow_trinket import WowTrinket


class Dungeon(base.StaticModel):
    """A Dungeon in the Game.

    With an `id`, a whole run of it (one Warcraft Logs encounter) loads as a Fight in User Reports.
    Dungeons are never ranked.
    """

    id: int = 0
    """Warcraft Logs encounter id of a whole run. 0: runs of this dungeon are not loaded."""

    name: str
    """Full Name."""

    trinkets: list[WowTrinket] = []
    """List of (relevant) Trinkets that drop from Bosses inside the Dungeon."""

    @property
    def name_slug(self) -> str:
        return utils.slug(self.name, space="-")
