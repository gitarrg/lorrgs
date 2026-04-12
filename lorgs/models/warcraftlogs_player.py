from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.models.warcraftlogs_actor import BaseActor
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


class Player(BaseActor):
    """A PlayerCharacter in a Fight (or report)."""

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
            "casts": [cast.model_dump() for cast in self.casts],
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
    # Process (kept for UserReport flow via Fight.process_players)
    #
    def process_death_events(self, death_events: list) -> None:
        """Add the Death Events to the Player."""
        from lorgs.clients import wcl

        self.deaths = []
        for death_event in death_events:
            if not isinstance(death_event, wcl.DeathEvent):
                continue
            target_id = death_event.id
            if self._has_source_id and (target_id != self.source_id):
                continue

            death_ability = death_event.ability
            death_data = {
                "ts": death_event.deathTime,
                "spell_name": death_ability.name,
                "spell_icon": death_ability.abilityIcon,
            }
            self.deaths.append(death_data)
