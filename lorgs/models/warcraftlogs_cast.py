from __future__ import annotations

# IMPORT STANDARD LIBRARIES
from collections import defaultdict
from typing import TYPE_CHECKING, Optional
import typing

# IMPORT THIRD PARTY LIBRARIES
import pydantic

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models import base
from lorgs.models.wow_spell import WowSpell


if TYPE_CHECKING:
    from lorgs.clients import wcl


# Maps Warcraftlogs Event Types to their corresponding ingame Comabatlog Event Types
WCL_TO_MRT_EVENT = {
    "cast": "SPELL_CAST_SUCCESS",
    "begincast": "SPELL_CAST_START",
    "applybuff": "SPELL_AURA_APPLIED",
    "applydebuff": "SPELL_AURA_APPLIED",
    "removebuff": "SPELL_AURA_REMOVED",
    "removedebuff": "SPELL_AURA_REMOVED",
    "death": "UNIT_DIED",
}

# Maps Combatlog Event Names to their shorthand versions used in MRT
MRT_EVENT_ABBREVIATION = {
    "SPELL_CAST_START": "SCS",
    "SPELL_CAST_SUCCESS": "SCC",
    "SPELL_AURA_APPLIED": "SAA",
    "SPELL_AURA_REMOVED": "SAR",
    "UNIT_DIED": "UD",
    "UNIT_SPELLCAST_START": "USS",
    "UNIT_SPELLCAST_SUCCEEDED": "USC",
    "CHAT_MSG_MONSTER_YELL": "CMMY",
}


class Cast(base.BaseModel):
    """An Instance of a Cast of a specific Spell in a Fight."""

    spell_id: int = pydantic.Field(alias="id")
    """ID of the spell/aura."""

    timestamp: int = pydantic.Field(alias="ts")
    """time the spell was cast, in milliseconds relative to the start of the fight."""

    duration: Optional[int] = pydantic.Field(default=None, alias="d")
    """time the spell/buff was active in milliseconds."""

    counter: int = pydantic.Field(default=0, alias="c")
    """Counter which instance of this type of event/spell_id has occurred in the current fight."""

    event_type: str = pydantic.Field(default="cast", exclude=True)

    model_config = pydantic.ConfigDict(populate_by_name=True)

    #############################

    @classmethod
    def from_report_event(cls, event: "wcl.ReportEvent") -> "Cast":
        spell_id = WowSpell.resolve_spell_id(event.abilityGameID, event.type)
        return cls(
            spell_id=spell_id,
            timestamp=event.timestamp,
            event_type=event.type,
        )

    def model_dump(self, **kwargs: typing.Any) -> dict[str, typing.Any]:
        kwargs.setdefault("by_alias", True)
        kwargs.setdefault("exclude_unset", True)
        return super().model_dump(**kwargs)

    def __str__(self):
        time_fmt = utils.format_time(self.timestamp)
        return f"Cast(id={self.spell_id}, ts={time_fmt})"

    @property
    def spell(self) -> Optional[WowSpell]:
        return WowSpell.get(spell_id=self.spell_id)

    @property
    def combatlog_event_type(self) -> str:
        return WCL_TO_MRT_EVENT.get(self.event_type, "UNKNOWN")

    @property
    def mrt_trigger(self) -> str:
        """eg.: SCC:442432:1"""
        event = MRT_EVENT_ABBREVIATION.get(self.combatlog_event_type, self.combatlog_event_type)
        return f"{event}:{self.spell_id}:{self.counter}"

    def get_duration(self) -> int:
        if self.duration:
            return self.duration

        if self.spell:
            return int(self.spell.duration * 1000)

        return 0

    ############################################################################
    # Cast Processing functions
    #
    def convert_to_start_event(self) -> None:
        """Convert this Cast into a start event.

        eg.: Convert from "remove debuff" to "apply debuff"
        and automatically shift the timestamp based on the spell default duration
        """
        duration = self.get_duration()
        if not duration:
            # TMP hack for eg.: Phase Events, where we're only interested in remove event
            return

        self.event_type = self.event_type.replace("remove", "apply")
        self.timestamp -= duration


def process_auras(events: list[Cast]) -> list[Cast]:
    """Calculate Aura Durations from "applybuff" to "applydebuff".

    Also converts "removebuff" events without matching "apply"
    eg.: a "removebuff" from an Aura that got applied prepull

    """
    # spell id --> application event
    active_buffs: dict[int, Cast] = {}

    for event in events:
        spell_id = event.spell_id

        # track the applications (pref initial)
        if event.event_type in ("applybuff", "applydebuff"):
            # Buffs with predefined/fixed duration need to custom logic.
            # we can simply pass over them here

            # (2024/03/04): due to the recent prepull buff change, we always track apply and remove events.
            # if event.get_duration() > 0:
            #     continue

            if event.spell_id in active_buffs:  # this is already tracked
                event.spell_id = -1
                continue

            active_buffs[spell_id] = event
            continue

        if event.event_type in ("removebuff", "removedebuff"):
            start_event = active_buffs.get(spell_id)

            # calc dynamic duration from start -> end
            if start_event:
                start_event.duration = event.timestamp - start_event.timestamp
                active_buffs.pop(event.spell_id)
                event.spell_id = -1
            else:
                # Automatically create start event
                event.convert_to_start_event()

    return [event for event in events if event.spell_id >= 0]


def process_until_events(casts: list[Cast]) -> list[Cast]:
    """Dynamically set the duration from the corresponding "until"-event."""

    for cast in casts:
        spell = cast.spell
        if not (spell and spell.until):
            continue

        # find valid "until"-events
        end_events = [e for e in casts if (e.timestamp > cast.timestamp) and (e.spell_id == spell.until.spell_id)]
        if not end_events:
            continue

        end_event = end_events[0]
        end_event.spell_id = -1  # flag for filtering
        cast.duration = end_event.timestamp - cast.timestamp

    return [c for c in casts if c.spell_id > 0]


def add_cast_counters(events: list[Cast]) -> list[Cast]:
    """Adds a counter to each event, tracking how many times
    each (event_type, spell_id) pair has occurred.

    Args:
        casts (list[Cast]): A list of cast events.

    Returns:
        list[Cast]: The same list with an added 'counter' attribute for each cast.

    """
    counters: dict[tuple[str, int], int] = defaultdict(int)

    for cast in events:
        key = (cast.event_type, cast.spell_id)

        counters[key] += 1
        cast.counter = counters[key]

    return events
