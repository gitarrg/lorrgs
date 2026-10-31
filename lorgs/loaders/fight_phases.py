from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import textwrap
import typing
from typing import TYPE_CHECKING

# IMPORT LOCAL LIBRARIES
from lorgs.clients import wcl
from lorgs.logger import logger
from lorgs.models.warcraftlogs_cast import Cast
from lorgs.models.wow_spell import build_spell_query

from .base_loader import BaseLoader


if TYPE_CHECKING:
    from lorgs.clients.wcl import WarcraftlogsClient
    from lorgs.models.game_data import GameData
    from lorgs.models.raid_boss import RaidBoss
    from lorgs.models.warcraftlogs_fight import Fight, Phase


class FightPhasesLoader(BaseLoader):
    """Loader for fight phases.

    This loads only the phases for the fight, together with the boss Casts
    the boss's phase correction needs (`RaidBoss.phase_spells`).
    Mostly used for spec rankings.

    """

    def __init__(self, fight: Fight, game_data: GameData) -> None:
        super().__init__(game_data)
        self.fight = fight

    def _raid_boss(self) -> RaidBoss | None:
        """The Actor Type of the Fight's boss, looked up in the Game Data."""
        if self.fight.boss is None:
            return None
        return self.game_data.get_boss(full_name_slug=self.fight.boss.boss_slug)

    def needs_casts(self) -> bool:
        """True when the boss corrects its Phases from Casts, so transitions alone are not enough."""
        raid_boss = self._raid_boss()
        return bool(raid_boss and raid_boss.phase_spells)

    def get_report_fields(self) -> str:
        """The fields inside `report { ... }` this loader needs. Shared with `FightLoader`."""
        fields = textwrap.dedent(
            f"""\
            fights(fightIDs: {self.fight.fight_id})
            {{
                phaseTransitions
                {{
                    id
                    startTime
                }}
            }}
            """,
        )

        raid_boss = self._raid_boss()
        if raid_boss and raid_boss.phase_spells:
            spells = [spell for spell in raid_boss.all_spells if spell.spell_id in raid_boss.phase_spells]
            fields += textwrap.dedent(
                f"""\
                events({self.fight.table_query_args}, filterExpression: "{build_spell_query(*spells)}")
                {{
                    data
                }}
                """,
            )
        return fields

    def get_query(self) -> str:
        if not self.fight.report:
            raise ValueError("Missing Parent Report")

        return f'reportData {{ report(code: "{self.fight.report.report_id}") {{ {self.get_report_fields()} }} }}'

    def process_phase_transitions(
        self,
        phase_transitions: list[wcl.PhaseTransition],
        casts: list[Cast] | None = None,
    ) -> None:
        """Set the Fight's Phases from the transitions, corrected by the boss from its phase Casts."""
        raid_boss = self._raid_boss()
        if not raid_boss:
            return

        phases: list[Phase] = []
        for phase_transition in phase_transitions:
            start_time = self.fight.to_fight_time(phase_transition.startTime)
            converted = phase_transition.model_copy(update={"startTime": start_time})

            if phase := raid_boss.phase_from_transition(converted):
                phases.append(phase)

        try:
            phases = raid_boss.process_phases(phases, casts or [])
        except Exception:  # ruff: ignore[blind-except]  # one boss must not fail the load
            logger.exception("Failed to correct phases for fight %s", self.fight.fight_id)

        for phase in phases:
            self.fight.add_phase(phase)

    def process_query_result(self, query_result: dict[str, typing.Any]) -> None:
        report = wcl.ReportData(**query_result).report

        phase_transitions = [
            phase_transition
            for fight in report.fights
            if fight.id in {self.fight.fight_id, -1}
            for phase_transition in fight.phaseTransitions
        ]
        casts = [
            Cast(spell_id=event.abilityGameID, timestamp=self.fight.to_fight_time(event.timestamp))
            for event in report.events
        ]
        self.process_phase_transitions(phase_transitions, casts)

    def needs_load(self) -> bool:
        if self.fight.phases:
            return False
        if not (raid_boss := self._raid_boss()):
            return False
        return raid_boss.phase_type == raid_boss.PhaseType.DYNAMIC

    async def load(self, client: WarcraftlogsClient | None = None) -> None:
        """Load the data for the actor."""
        self.fight.event_fight_phases_load.send(self.fight, status="start")
        try:
            await super().load(client=client)
        except:
            self.fight.event_fight_phases_load.send(self.fight, status="failed")
            raise
        else:
            self.fight.event_fight_phases_load.send(self.fight, status="success")
