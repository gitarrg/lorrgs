"""Loaders for Actor (Player / Boss) data from WarcraftLogs."""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.models.wow_spell import WowSpell, build_spell_query

from .actor_loader import ActorLoader


if typing.TYPE_CHECKING:
    from lorgs.clients import wcl
    from lorgs.models.warcraftlogs_player import Player


def _combine_queries(*queries: str, op: str = "or") -> str:
    """Combine multiple queries.

    Essentially just wraps them in parentheses and joins
    them with the given operator.

    Example:
        >>> _combine_queries("foo", "bar", "baz", op="and")
        "((foo) and (bar) and (baz))"

        >>> _combine_queries("foo", "bar", "baz", op="or")
        "((foo) or (bar) or (baz))"

    """
    queries: list[str] = list(queries)
    queries = [q for q in queries if q]
    queries = [f"({q})" for q in queries]
    queries_combined = f" {op} ".join(queries)
    return f"({queries_combined})"


class PlayerLoader(ActorLoader):
    """Loader for Player actors with player-specific filtering."""

    actor: Player

    def __init__(self, actor: Player) -> None:
        super().__init__(actor)

    ############################################################################
    #
    # Query
    #
    ############################################################################

    def get_sub_query(self) -> str:
        actor_type = self.actor.actor_type

        casts_query = build_spell_query(*actor_type.all_spells)
        if casts_query and self.actor.name:
            casts_query = f"source.name='{self.actor.name}' and ({casts_query})"

        auras_query = build_spell_query(*actor_type.all_buffs, *actor_type.all_debuffs)
        if auras_query and self.actor.name:
            auras_query = f"target.name='{self.actor.name}' and ({auras_query})"

        events_query = build_spell_query(*actor_type.all_events)
        if events_query and self.actor.name:
            events_query = f"source.name='{self.actor.name}' and ({events_query})"

        resurrection_query = ""
        if self.actor.resurrects and self.actor.name:
            resurrection_query = f"target.name='{self.actor.name}' and type='resurrect'"

        return _combine_queries(casts_query, auras_query, events_query, resurrection_query)

    ############################################################################
    #
    # Process
    #
    ############################################################################

    def _set_source_id_from_events(self, events: list[wcl.ReportEvent]) -> None:
        """Set the Source ID from the cast data.

        In some cases (eg.: data pulled from spec rankings) we don't know the source ID upfront..
        but we can fill that gap here
        """
        if self.actor.source_id > 0:
            return
        for event in events:
            if event.type == "cast":
                self.actor.source_id = event.sourceID
            if self.actor.source_id > 0:
                return

    def process_events(self, events: list[wcl.ReportEvent]) -> list[wcl.ReportEvent]:
        """Hook to preprocess the entire list of  Cast/Events.

        Args:
            events (list[wcl.ReportEvent]): The list of Events to be processed

        Returns:
            events (list[wcl.ReportEvent]): The processed list of Events

        """
        self._set_source_id_from_events(events)
        return super().process_events(events)

    def process_event(self, event: wcl.ReportEvent) -> wcl.ReportEvent:
        spell_id = event.abilityGameID

        # special case: Ankh
        if spell_id == 21169:   # noqa: PLR2004
            event.type = "resurrect"

        if event.type == "resurrect":
            self._process_resurrect(event)
            event.abilityGameID = -1

        return super().process_event(event)

    def _process_resurrect(self, event: wcl.ReportEvent) -> None:
        fight_start = self.actor.fight.start_time_rel if self.actor.fight else 0

        data: dict[str, typing.Any] = {}
        data["ts"] = event.timestamp - fight_start

        spell_id = event.abilityGameID
        spell = WowSpell.get(spell_id=spell_id)
        if spell:
            data["spell_name"] = spell.name
            data["spell_icon"] = spell.icon

        # new list so that pydantic's "exclude unset" doesn't exclude it.
        if not self.actor.resurrects:
            self.actor.resurrects = []

        # Look for the Source ID
        source_id = event.sourceID
        if self.actor.fight and self.actor.fight.report:
            source_player = self.actor.fight.get_player(source_id=source_id)
            if source_player:
                data["source_name"] = source_player.name
                data["source_class"] = source_player.class_slug

        self.actor.resurrects.append(data)
