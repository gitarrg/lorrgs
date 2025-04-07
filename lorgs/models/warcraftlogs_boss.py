from __future__ import annotations

# IMPORT STANDARD LIBRARIES
from collections import defaultdict
import enum
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.clients import wcl
from lorgs.models import warcraftlogs_actor
from lorgs.models.raid_boss import RaidBoss
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

        # lookup table for phase triggers based on (spell_id, event_type, count)
        triggers = {(trigger.spell_id, trigger.event_type, trigger.count): trigger for trigger in self.raid_boss.phases}

        for event in events:

            counters[(event.abilityGameID, event.type)] += 1
            count = counters[(event.abilityGameID, event.type)]

            # check if this event triggers a new phase.
            # key = [spellID, eventType, count], where count may be 0 if every occurrence
            # triggers a new phase
            trigger = triggers.get((event.abilityGameID, event.type, count)) or triggers.get((event.abilityGameID, event.type, 0))
            if not trigger:
                continue

            # if a trigger count is set, compare it to the event count
            if trigger.count and count is not trigger.count:
                continue

            cast = Cast.from_report_event(event)
            cast.timestamp -= self.fight.start_time_rel
            cast.counter = count

            self.fight.add_phase(
                ts=cast.timestamp,
                name=trigger.name,
                mrt=cast.mrt_trigger,
                count=count,
            )

    def process_events(self, events: list[wcl.ReportEvent]) -> list[wcl.ReportEvent]:
        self.process_phase_events(events)
        return events
