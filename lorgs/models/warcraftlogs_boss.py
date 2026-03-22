from __future__ import annotations

# IMPORT STANDARD LIBRARIES
from collections import defaultdict
import enum
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.clients import wcl
from lorgs.models import warcraftlogs_actor
from lorgs.models.raid_boss import Phase, RaidBoss
from lorgs.models.warcraftlogs_cast import Cast
from lorgs.models.wow_spell import WowSpell


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

    ############################################################################
    #
    # Query
    #
    ############################################################################

    def get_query_abilities(self) -> list[WowSpell]:
        """Get all abilities to be queried."""
        if self.query_mode == self.QueryModes.PHASES:
            return self.raid_boss.phases  # type: ignore

        return [
            *super().get_query_abilities(),
            *self.raid_boss.phases,
        ]

    def process_phase_events(self, events: list[wcl.ReportEvent]) -> None:

        if not self.fight:
            return

        # clear out any old data
        # not sure if we'd ever want to keep old data,
        # or at least leave this in case we're adding phases in a different way
        if self.fight.phases:
            self.fight.phases = []

        counters: dict[tuple[int, str], int] = defaultdict(int)

        # Ordered triggers per (spell_id, event_type). A dict on (spell_id, event_type, count)
        # drops duplicates when the same signal is used for more than one phase.
        phases_by_key: dict[tuple[int, str], list[Phase]] = defaultdict(list)
        for phase in self.raid_boss.phases:
            phases_by_key[(phase.spell_id, phase.event_type)].append(phase)

        for event in events:
            key = (event.abilityGameID, event.type)
            counters[key] += 1
            count = counters[key]

            triggers = phases_by_key.get(key)
            if not triggers:
                continue

            for trigger in triggers:
                cast = Cast.from_report_event(event)
                cast.timestamp -= self.fight.start_time_rel
                cast.counter = count

                self.fight.add_phase(
                    ts=cast.timestamp + trigger.offset,
                    name=trigger.name,
                    mrt=cast.mrt_trigger,
                    count=count,
                )

    def process_events(self, events: list[wcl.ReportEvent]) -> list[wcl.ReportEvent]:
        self.process_phase_events(events)
        return events
