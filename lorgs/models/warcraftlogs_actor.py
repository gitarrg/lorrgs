from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import abc
import textwrap
import typing
from typing import ClassVar, Optional

# IMPORT THIRD PARTY LIBRARIES
import blinker
import pydantic

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.clients import wcl
from lorgs.logger import logger
from lorgs.models import warcraftlogs_base
from lorgs.models.warcraftlogs_cast import Cast, process_auras, process_until_events, add_cast_counters
from lorgs.models.wow_spell import SpellType, WowSpell, build_spell_query


if typing.TYPE_CHECKING:
    from lorgs.models.warcraftlogs_fight import Fight
    from lorgs.models.wow_actor import WowActor


class BaseActor(warcraftlogs_base.BaseModel):
    """Base Class for any Actor in a Fight.

    these are usually either Players or NPC/Bosses

    """

    source_id: int = -1
    casts: list[Cast] = []

    fight: Optional["Fight"] = pydantic.Field(exclude=True, default=None, repr=False)

    # Events
    event_actor_load: ClassVar[blinker.Signal] = blinker.signal("actor.load")

    ############################################################################
    #
    # Attributes
    #
    ############################################################################

    @property
    def _has_source_id(self) -> bool:
        return self.source_id >= 0

    @property
    def has_own_casts(self) -> bool:
        """Return true if a player has own casts (eg.: exclude raid wide buffs like bloodlust)."""
        for cast in self.casts:
            spell = WowSpell.get(spell_id=cast.spell_id)
            if spell and spell.spell_type != SpellType.BUFF:
                return True
        return False

    @abc.abstractmethod
    def get_actor_type(self) -> "WowActor":
        """Get the Type of Actor."""

    @property
    def actor_type(self) -> "WowActor":
        return self.get_actor_type()

    async def load(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        self.event_actor_load.send(self, status="start")
        try:
            await super().load(*args, **kwargs)
        except:
            self.event_actor_load.send(self, status="failed")
            raise
        else:
            self.event_actor_load.send(self, status="success")

    ############################################################################
    #
    # Query
    #
    ############################################################################

    def get_query_abilities(self) -> list[WowSpell]:
        """Get all abilities to be queried."""
        return [
            *self.actor_type.all_spells,
            *self.actor_type.all_buffs,
            *self.actor_type.all_debuffs,
            *self.actor_type.all_events,
        ]

    def get_sub_query(self) -> str:
        """Get the Query for fetch all relevant data for this actor."""
        # combine all parts
        abilities = self.get_query_abilities()
        query = build_spell_query(*abilities)
        return query

    def get_query(self) -> str:
        if not self.fight:
            raise ValueError("missing fight")
        if not self.fight.report:
            raise ValueError("missing report")

        sub_query = self.get_sub_query()
        if not sub_query:
            # eg.: a boss in `query_mode.phases` but with not phase-triggers
            return

        return textwrap.dedent(
            f"""\
            reportData
            {{
                report(code: "{self.fight.report.report_id}")
                {{
                    events({self.fight.table_query_args}, filterExpression: "{sub_query}")
                        {{data}}
                }}
            }}
        """
        )

    ############################################################################
    #
    # Process
    #
    ############################################################################

    def process_events(self, events: list[wcl.ReportEvent]) -> list[wcl.ReportEvent]:
        """Hook to preprocess the entire list of  Cast/Events.

        Args:
            events (list[wcl.ReportEvent]): The list of Events to be processed

        Returns:
            events (list[wcl.ReportEvent]): The processed list of Events

        """
        return events

    def process_event(self, event: wcl.ReportEvent) -> wcl.ReportEvent:
        """Hook to preprocess each Cast/Event

        Args:
            event (wcl.ReportEvent): The Event to be processed

        Returns:
            event (wcl.ReportEvent): The processed Event

        """
        return event

    def set_source_id_from_events(self, casts: list[wcl.ReportEvent], force=False):
        """Set the Source ID from the cast data.

        In some cases (eg.: data pulled from spec rankings) we don't know the source ID upfront..
        but we can fill that gap here
        """
        if force == False and self._has_source_id:
            return

        for cast in casts:
            if cast.type == "cast":
                self.source_id = cast.sourceID

            # return as soon as we have a value
            if self.source_id > 0:
                return

    def process_query_result(self, **query_data: typing.Any) -> None:
        """Process the result of a casts-query to create Cast objects."""
        query_data = query_data.get("reportData") or query_data
        report_data = wcl.ReportData(**query_data)
        casts_data = report_data.report.events

        if not casts_data:
            logger.warning("casts_data is empty")
            return

        ##############################
        # Pre Processing
        self.set_source_id_from_events(casts_data)
        casts_data = self.process_events(casts_data)

        ##############################
        # Main
        for cast_data in casts_data:
            cast_data = self.process_event(cast_data)

            # Some Types (eg.: Buffs) are tracked based on the target.
            # eg.: PowerInfusion shows on the Target, not the Priest.
            cast_actor_id = cast_data.sourceID
            if cast_data.type in ("applybuff", "removebuff", "resurrect"):
                cast_actor_id = cast_data.targetID

            # Skip if the Source ID doesn't match
            if self._has_source_id and (cast_actor_id != self.source_id):
                continue

            # create the cast object
            cast = Cast.from_report_event(cast_data)
            cast.timestamp -= self.fight.start_time_rel if self.fight else 0
            self.casts.append(cast)

        ##############################
        # Post Processing
        self.casts = process_until_events(self.casts)
        self.casts = process_auras(self.casts)

        # Filter out same event at the same time (eg.: raid wide debuff apply)
        self.casts = utils.uniqify(self.casts, key=lambda cast: (cast.spell_id, int(cast.timestamp / 1000)))

        # make sure casts are sorted correctly
        # avoids weird UI overlaps, and just feels cleaner
        self.casts = sorted(self.casts, key=lambda cast: cast.timestamp)

        # we do this at the very end after all the filtering has been done.
        self.casts = add_cast_counters(self.casts)
