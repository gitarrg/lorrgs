# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base
from lorgs.models.wow_trinket import WowTrinket


FALLBACK_ICON = "inv_misc_map_01.jpg"
"""Icon of every Dungeon without one of its own (a map)."""


class Dungeon(base.StaticModel):
    """A Dungeon in the Game.

    With an `id`, a whole run of it (one Warcraft Logs encounter) loads as a Fight in User Reports.
    Dungeons are never ranked.
    """

    id: int = 0
    """Warcraft Logs encounter id of a whole run. 0: runs of this dungeon are not loaded."""

    name: str
    """Full Name."""

    par_time: float = 0
    """Mythic+ timer in seconds: a run within it is timed (+2 within 80% of it, +3 within 60%).
    From DB2 `MapChallengeMode.CriteriaCount_0`. 0: unknown."""

    icon: str = FALLBACK_ICON
    """Icon file in the shared spell icon folder. All Dungeons share a fallback until they get their own."""

    trinkets: list[WowTrinket] = []
    """List of (relevant) Trinkets that drop from Bosses inside the Dungeon."""

    @property
    def name_slug(self) -> str:
        return utils.slug(self.name, space="-")

    def as_dict(self) -> dict:
        """The Dungeon as the frontend needs it to label a run (not its trinkets)."""
        return {
            "id": self.id,
            "name": self.name,
            "name_slug": self.name_slug,
            "icon": self.icon,
            "par_time": self.par_time,
        }
