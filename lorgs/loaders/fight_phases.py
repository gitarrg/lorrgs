from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import textwrap
import typing
from typing import TYPE_CHECKING

# IMPORT LOCAL LIBRARIES
from lorgs.clients import wcl
from lorgs.logger import logger

from .base_loader import BaseLoader


if TYPE_CHECKING:
    from lorgs.clients.wcl import WarcraftlogsClient
    from lorgs.models.warcraftlogs_fight import Fight


def correct_loaded_phases(fight: Fight) -> None:
    """Apply the boss's phase correction once its Casts are loaded.

    A failure is logged and the Fight's Phases stay as they were.
    """
    boss = fight.boss
    if boss is None:
        return

    try:
        fight.phases = boss.raid_boss.process_phases(fight.phases, boss.casts)
    except Exception:  # ruff: ignore[blind-except]  # one boss must not fail the load
        logger.exception("Failed to correct phases for fight %s", fight.fight_id)


class FightPhasesLoader(BaseLoader):
    """Loader for fight phases.

    This loads only the phases for the fight.
    Mostly used for spec rankings.

    """

    def __init__(self, fight: Fight) -> None:
        self.fight = fight

    def get_query(self) -> str:
        if not self.fight.report:
            raise ValueError("Missing Parent Report")

        return textwrap.dedent(
            f"""\
            reportData
            {{
                report(code: "{self.fight.report.report_id}")
                {{
                    fights(fightIDs: {self.fight.fight_id})
                    {{
                        phaseTransitions
                        {{
                            id
                            startTime
                        }}
                    }}
                }}
            }}
            """,
        )

    def process_phase_transitions(self, phase_transitions: list[wcl.PhaseTransition]) -> None:

        if not phase_transitions:
            return

        raid_boss = self.fight.boss.raid_boss if self.fight.boss else None
        if not raid_boss:
            return

        for phase_transition in phase_transitions:

            start_time = self.fight.to_fight_time(phase_transition.startTime)
            converted = phase_transition.model_copy(update={"startTime": start_time})

            if phase := raid_boss.phase_from_transition(converted):
                self.fight.add_phase(phase)

    def process_query_result(self, query_result: dict[str, typing.Any]) -> None:
        report_data = wcl.ReportData(**query_result)

        for fight in report_data.report.fights:
            if fight.id not in {self.fight.fight_id, -1}:
                continue

            self.process_phase_transitions(fight.phaseTransitions)

    def needs_load(self) -> bool:
        if self.fight.phases:
            return False
        if not (boss := self.fight.boss):
            return False
        if not (raid_boss := boss.raid_boss):
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
