from __future__ import annotations

# IMPORT STANRD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.clients import wcl
from lorgs.models.warcraftlogs_actor import BaseActor
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import WowSpell, build_spell_query


class Player(BaseActor):
    """A PlayerCharater in a Fight (or report)."""

    name: str = ""
    class_slug: str = ""
    spec_slug: str = ""

    total: float = 0

    deaths: list = []
    resurrects: list = []

    def __str__(self) -> str:
        return f"Player(id={self.source_id} name={self.name} spec={self.spec})"

    def summary(self) -> dict[str, typing.Any]:
        return {
            "name": self.name,
            "source_id": self.source_id,
            "class": self.class_slug,
            "spec": self.spec_slug,
            "role": self.spec.role.code if self.spec else "",
        }

    def as_dict(self) -> dict[str, typing.Any]:
        return {
            **self.summary(),
            "total": int(self.total),
            "casts": [cast.dict() for cast in self.casts],
            "deaths": self.deaths,
            "resurrects": self.resurrects,
        }

    ##########################
    # Attributes
    #
    @property
    def class_(self) -> WowClass:
        return WowClass.get(name_slug=self.class_slug)  # type: ignore

    @property
    def spec(self) -> WowSpec:
        return WowSpec.get(full_name_slug=self.spec_slug)  # type: ignore

    def get_actor_type(self):
        return self.spec

    ############################################################################
    # Query
    #

    def get_sub_query(self):

        # Casts
        casts_query = build_spell_query(*self.actor_type.all_spells)
        if casts_query and self.name:
            casts_query = f"source.name='{self.name}' and ({casts_query})"

        # Auras
        auras_query = build_spell_query(*self.actor_type.all_buffs, *self.actor_type.all_debuffs)
        if auras_query and self.name:
            auras_query = f"target.name='{self.name}' and ({auras_query})"

        # Events
        events_query = build_spell_query(*self.actor_type.all_events)
        if events_query and self.name:
            events_query = f"source.name='{self.name}' and ({events_query})"

        resurrection_query = ""
        if self.resurrects and self.name:
            resurrection_query = f"target.name='{self.name}' and type='resurrect'"

        return self.combine_queries(casts_query, auras_query, events_query, resurrection_query)

    ############################################################################
    # Process
    #

    def process_death_events(self, death_events: list[wcl.DeathEvent]):
        """Add the Death Events the the Players.

        Args:
            death_events[list[dict]]

        """

        # TODO: add during model validation?
        # ABILITY_OVERWRITES = {}
        # ABILITY_OVERWRITES[1] = {"name": "Melee", "guid": 260421, "abilityIcon": "ability_meleedamage.jpg"}
        # ABILITY_OVERWRITES[3] = {"name": "Fall Damage"}

        # new list so that pydantic's "exclude unset" doesn't exclude it.
        self.deaths = []

        for death_event in death_events:
            target_id = death_event.id
            if self._has_source_id and (target_id != self.source_id):
                continue

            death_ability = death_event.ability
            # death_ability_id = death_ability.guid
            # death_ability = ABILITY_OVERWRITES.get(death_ability_id) or death_ability

            death_data = {
                "ts": death_event.deathTime,
                "spell_name": death_ability.name,
                "spell_icon": death_ability.abilityIcon,
            }
            self.deaths.append(death_data)

    def process_event_resurrect(self, event: "wcl.ReportEvent"):
        fight_start = self.fight.start_time_rel if self.fight else 0

        data: dict[str, typing.Any] = {}
        data["ts"] = event.timestamp - fight_start

        spell_id = event.abilityGameID
        spell = WowSpell.get(spell_id=spell_id)
        if spell:
            data["spell_name"] = spell.name
            data["spell_icon"] = spell.icon

        # new list so that pydantic's "exclude unset" doesn't exclude it.
        self.resurrects = []

        # Look for the Source ID
        source_id = event.sourceID
        if self.fight and self.fight.report:
            source_player = self.fight.get_player(source_id=source_id)
            if source_player:
                data["source_name"] = source_player.name
                data["source_class"] = source_player.class_slug

        self.resurrects.append(data)

    def process_event(self, event: "wcl.ReportEvent") -> wcl.ReportEvent:
        # Ankh doesn't shows as a regular spell
        spell_id = event.abilityGameID
        if spell_id in (21169,):  # Ankh
            event.type = "resurrect"

        if event.type == "resurrect":
            self.process_event_resurrect(event)
            event.abilityGameID = -1

        return super().process_event(event)
