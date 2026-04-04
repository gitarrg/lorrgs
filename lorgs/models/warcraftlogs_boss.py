from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import enum
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.models import warcraftlogs_actor
from lorgs.models.raid_boss import RaidBoss


if typing.TYPE_CHECKING:
    from lorgs.models.wow_actor import WowActor


class Boss(warcraftlogs_actor.BaseActor):
    """A NPC/Boss in a Fight."""

    boss_slug: str

    class QueryModes(enum.Enum):
        ALL = 0
        SPELLS = 1
        PHASES = 2

    query_mode: QueryModes = QueryModes.ALL

    ##########################
    # Attributes
    #
    def __str__(self):
        return f"Boss(slug={self.boss_slug})"

    @property
    def raid_boss(self) -> RaidBoss:
        raid_boss = RaidBoss.get(full_name_slug=self.boss_slug)
        if not raid_boss:
            raise ValueError(f"Invalid boss_slug: {self.boss_slug}")
        return raid_boss

    def get_actor_type(self) -> "WowActor":
        return self.raid_boss

    @classmethod
    def from_raid_boss(cls, raid_boss: RaidBoss) -> "Boss":
        return cls(boss_slug=raid_boss.full_name_slug)

    def as_dict(self) -> dict[str, typing.Any]:
        return {
            "name": self.raid_boss and self.raid_boss.full_name_slug,
            "casts": [cast.model_dump() for cast in self.casts],
        }

    def set_source_id_from_events(self, *args, **kwargs):
        """Do nothing here, to avoid issues with Council Boss Fights."""
        pass

