"""Loaders for Actor (Player / Boss) data from WarcraftLogs."""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import textwrap
import typing

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.clients import wcl
from lorgs.loaders.base_loader import BaseLoader
from lorgs.models.warcraftlogs_cast import Cast, add_cast_counters, process_auras, process_until_events
from lorgs.models.wow_spell import WowSpell, build_spell_query


if typing.TYPE_CHECKING:
    from lorgs.clients.wcl import WarcraftlogsClient
    from lorgs.models.warcraftlogs_actor import BaseActor


class ActorLoader(BaseLoader):
    """Loads event data for a single actor from WarcraftLogs."""

    def __init__(self, actor: BaseActor) -> None:
        self.actor = actor
        self.actor_type = actor.actor_type

    def needs_load(self) -> bool:
        """Check if the data needs to be loaded."""
        return len(self.actor.casts) == 0

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
        fight = self.actor.fight
        if not fight:
            raise ValueError("missing fight")
        if not fight.report:
            raise ValueError("missing report")

        sub_query = self.get_sub_query()
        if not sub_query:
            return ""

        return textwrap.dedent(
            f"""\
            reportData
            {{
                report(code: "{fight.report.report_id}")
                {{
                    events({fight.table_query_args}, filterExpression: "{sub_query}")
                        {{data}}
                }}
            }}
        """)

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
        """Hook to preprocess each Cast/Event.

        Args:
            event (wcl.ReportEvent): The Event to be processed

        Returns:
            event (wcl.ReportEvent): The processed Event

        """
        return event

    def process_query_result(self, query_result: dict[str, typing.Any]) -> None:
        query_result = query_result.get("reportData") or query_result
        report_data = wcl.ReportData(**query_result)
        casts_data = report_data.report.events

        if not casts_data:
            return

        ##############################
        # Pre Processing
        casts_data = self.process_events(casts_data)

        ##############################
        # Process Casts
        self.actor.casts = []
        for cast_data in casts_data:
            cast_data = self.process_event(cast_data)  # noqa: PLW2901

            # Some Types (eg.: Buffs) are tracked based on the target.
            # eg.: PowerInfusion shows on the Target, not the Priest.
            cast_actor_id = cast_data.sourceID
            if cast_data.type in ("applybuff", "removebuff", "resurrect"):
                cast_actor_id = cast_data.targetID

            # Skip if the Source ID doesn't match
            if self.actor.source_id > 0 and (cast_actor_id != self.actor.source_id):
                continue

            # create the cast object
            cast = Cast.from_report_event(cast_data)
            cast.timestamp -= self.actor.fight.start_time_rel if self.actor.fight else 0
            self.actor.casts.append(cast)

        ##############################
        # Post Processing
        self.actor.casts = process_until_events(self.actor.casts)
        self.actor.casts = process_auras(self.actor.casts)

        # Filter out same event at the same time (eg.: raid wide debuff apply)
        self.actor.casts = utils.uniqify(
            self.actor.casts,
            key=lambda cast: (cast.spell_id, int(cast.timestamp / 1000), cast.event_type),
        )

        # make sure casts are sorted correctly
        # avoids weird UI overlaps, and just feels cleaner
        self.actor.casts = sorted(self.actor.casts, key=lambda cast: cast.timestamp)

        # we do this at the very end after all the filtering has been done.
        self.actor.casts = add_cast_counters(self.actor.casts)

    def remove_buffs_from_casts(
        self,
        cast_spell_ids: set[int],
        buff_spell_ids: set[int],
        tolerance: int = 500,
    ) -> None:
        """Remove buffs that happen at the same time as a cast.

        for example Ascendance buffs at the same time as a casts.
        This helps to later identify manually cast buffs vs. procs.

        NOTE: currently unused

        """
        casts = [c for c in self.actor.casts if c.spell_id in cast_spell_ids and c.event_type == "cast"]
        buffs = [c for c in self.actor.casts if c.spell_id in buff_spell_ids and c.event_type == "applybuff"]
        if not casts and buffs:
            return

        for buff in buffs:
            closest = min(casts, key=lambda c: abs(c.timestamp - buff.timestamp))
            if abs(buff.timestamp - closest.timestamp) < tolerance:
                buff.spell_id = -1
        self.actor.casts = [c for c in self.actor.casts if c.spell_id > 0]

    ############################################################################
    # Load
    ############################################################################

    async def load(self, client: WarcraftlogsClient | None = None) -> None:
        """Load the data for the actor."""
        self.actor.event_actor_load.send(self.actor, status="start")
        try:
            await super().load(client=client)
        except:
            self.actor.event_actor_load.send(self.actor, status="failed")
            raise
        else:
            self.actor.event_actor_load.send(self.actor, status="success")
