from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.models import warcraftlogs_actor


if typing.TYPE_CHECKING:
    from lorgs.models.raid_boss import RaidBoss


class Boss(warcraftlogs_actor.BaseActor):
    """A NPC/Boss in a Fight."""

    boss_slug: str

    ##########################
    # Attributes
    #
    def __str__(self):
        return f"Boss(slug={self.boss_slug})"

    @classmethod
    def from_raid_boss(cls, raid_boss: RaidBoss) -> Boss:
        return cls(boss_slug=raid_boss.full_name_slug)

    def as_dict(self) -> dict[str, typing.Any]:
        return {
            "name": self.boss_slug,
            "casts": [cast.model_dump() for cast in self.casts],
        }
