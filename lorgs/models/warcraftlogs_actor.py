
# IMPORT STANRD LIBRARIES
import abc
from collections import defaultdict
import textwrap
import typing
import math

# IMPORT THIRD PARTY LIBRARIES
import mongoengine as me
import pydantic

# IMPORT LOCAL LIBRARIES
from lorgs import utils
# from lorgs.clients.wcl.models.query import Query
# from lorgs.clients.wcl.models.report_data import ReportData, ReportEvent
from lorgs.logger import logger
from lorgs.models import warcraftlogs_base
from lorgs.models.warcraftlogs_cast import Cast
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import EventSource, WowSpell

from lorgs.clients import wcl

if typing.TYPE_CHECKING:
    from lorgs.models.warcraftlogs_fight import Fight



class BaseActor(warcraftlogs_base.EmbeddedDocument):
    """Base Class for any Actor in a Fight.

    these are usually either Players or NPC/Bosses

    """

    casts: list[Cast] = me.ListField(me.EmbeddedDocumentField(Cast))

    source_id = -1

    meta = {
        'abstract': True,
    }

    def __init__(self, *args: typing.Any, **kwargs: typing.Any):
        super().__init__(*args, **kwargs)

        # backref to the parent fight object
        self.fight: typing.Optional["Fight"] = None

    ##########################
    # Attributes
    #
    @property
    def _has_source_id(self):
        return self.source_id >= 0

    @property
    def has_own_casts(self):
        """Return true if a player has own casts (eg.: exclude raid wide buffs like bloodlust)."""
        for cast in self.casts:
            spell = WowSpell.get(spell_id=cast.spell_id)

            if spell.spell_type != WowSpell.TYPE_BUFFS:
                return True
        return False

    #################################
    # Query
    #
    def get_event_query(self, spells: list[WowSpell]) -> str:
        """Generate the Query based of the given Spells.

        Generates a very verbose:
        ```
            "(type='spellA.type' and ability.id=spellA.spell_id) or (type='spellB.type' and ability.id=spellB.spell_id)"
        ```

        Args:
            spells WowSpell[]: List of Spells

        Returns:
            str: The Query
        """
        if not spells:
            return ""

        # TODO: group spells by event_type
        # spell_ids = WowSpell.spell_ids_str(spells)

        parts = []
        for spell in spells:
            part = f"(type='{spell.event_type}' and ability.id={spell.spell_id})"
            parts.append(part)

        return " or ".join(parts)

    def get_cast_query(self, spells: list[WowSpell]):
        if not spells:
            return ""

        spell_ids = WowSpell.spell_ids_str(spells)
        cast_filter = f"type='cast' and ability.id in ({spell_ids})"
        return cast_filter

    @staticmethod
    def _build_buff_query(spells: list[WowSpell], event_types: list[str]):
        if not spells:
            return ""
        spell_ids = WowSpell.spell_ids_str(spells)

        event_types = [f"'{event}'" for event in event_types] # wrap each into single quotes
        event_types_combined = ",".join(event_types)

        return f"type in ({event_types_combined}) and ability.id in ({spell_ids})"

    def get_buff_query(self, spells: list[WowSpell]):
        return self._build_buff_query(spells, ["applybuff", "removebuff"])

    def get_debuff_query(self, spells: list[WowSpell]):
        return self._build_buff_query(spells, ["applydebuff", "removedebuff"])

    @abc.abstractmethod
    def get_sub_query(self) -> str:
        return ""

    def get_query(self) -> str:
        if not self.fight:
            raise ValueError("missing fight")
        if not self.fight.report:
            raise ValueError("missing report")

        return textwrap.dedent(f"""\
            reportData
            {{
                report(code: "{self.fight.report.report_id}")
                {{
                    events({self.fight.table_query_args}, filterExpression: "{self.get_sub_query()}")
                        {{data}}
                }}
            }}
        """)

    #################################
    # Query
    #

    def process_event(self, event: wcl.ReportEvent):
        """Hook to preprocess Events

        Args:
            event (wcl.ReportEvent): The Event to be processed
        """
        pass

    @staticmethod
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
                if event.spell_id in active_buffs: # this is already tracked
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

        print("events", events)
        return [event for event in events if event.spell_id >= 0]

    def process_query_result(self, query_data: "wcl.Query") -> None:
        """Process the result of a casts-query to create Cast objects."""
        report_data = query_data.reportData
        if not report_data:
            return

        casts_data = report_data.report.events
        if not casts_data:
            logger.warning("casts_data is empty")
            return

        fight_start = self.fight.start_time_rel if self.fight else 0

        for cast_data in casts_data:
            self.process_event(cast_data)

            cast_type = cast_data.type or "unknown"

            # resurrect are dealt with in `process_event`
            if cast_type == "resurrect":
                continue

            # Some Types (eg.: Buffs) are tracked based on the target.
            # eg.: PowerInfusion shows on the Target, not the Priest.
            cast_actor_id = cast_data.sourceID
            if cast_type in ("applybuff", "removebuff", "resurrect"):
                cast_actor_id = cast_data.targetID

            # Skip if the Source ID doesn't match
            if self._has_source_id and (cast_actor_id != self.source_id):
                continue

            # Create the Cast Object
            self.casts.append(Cast(
                spell_id=cast_data.abilityGameID,
                timestamp=cast_data.timestamp - fight_start,
                duration=cast_data.duration,
            ))

        ##############################
        # Post Processing
        self.casts = self.process_auras(self.casts)

        # Filter out same event at the same time (eg.: raid wide debuff apply)
        self.casts = utils.uniqify(self.casts, key=lambda cast: (cast.spell_id, math.floor(cast.timestamp / 1000)))
        # self.casts = list(self.casts) # `utils.uniqify` returns dict values, which mongoengine doesn't like

        # make sure casts are sorted correctly
        # avoids weird UI overlaps, and just feels cleaner
        self.casts = sorted(self.casts, key=lambda cast: cast.timestamp)
