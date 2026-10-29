from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.models.warcraftlogs_actor import BaseActor

if typing.TYPE_CHECKING:
    from lorgs.clients import wcl
    from lorgs.models.game_data import GameData


class Player(BaseActor):
    """A PlayerCharacter in a Fight (or report)."""

    name: str = ""
    class_slug: str = ""
    spec_slug: str = ""

    total: float = 0

    deaths: list = []
    resurrects: list = []

    def __str__(self) -> str:
        return f"Player(id={self.source_id} name={self.name} spec={self.spec_slug})"

    def summary(self, game_data: GameData) -> dict[str, typing.Any]:
        spec = game_data.get_spec(self.spec_slug)
        return {
            "name": self.name,
            "source_id": self.source_id,
            "class": self.class_slug,
            "spec": self.spec_slug,
            "role": spec.role.code if spec else "",
        }

    def as_dict(self, game_data: GameData) -> dict[str, typing.Any]:
        return {
            **self.summary(game_data),
            "total": int(self.total),
            "casts": [cast.model_dump() for cast in self.casts],
            "deaths": self.deaths,
            "resurrects": self.resurrects,
        }

    ############################################################################
    # Process (kept for UserReport flow via Fight.process_players)
    #
    def process_death_events(self, death_events: list[wcl.DeathEvent]) -> None:
        """Add the Death Events to the Player."""
        self.deaths = []
        for death_event in death_events:
            target_id = death_event.id
            if self._has_source_id and (target_id != self.source_id):
                continue

            death_ability = death_event.ability
            death_time = death_event.deathTime
            if self.fight:
                death_time = self.fight.to_fight_time(death_time)
            death_data = {
                "ts": death_time,
                "spell_name": death_ability.name,
                "spell_icon": death_ability.abilityIcon,
            }
            self.deaths.append(death_data)
