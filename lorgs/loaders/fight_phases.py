from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import textwrap
import typing
from typing import TYPE_CHECKING

# IMPORT LOCAL LIBRARIES
from lorgs.clients import wcl

from .base_loader import BaseLoader


if TYPE_CHECKING:
    from lorgs.clients.wcl.client import WarcraftlogsClient
    from lorgs.models.warcraftlogs_fight import Fight


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
                            startTime
                        }}
                    }}
                }}
            }}
            """,
        )

    def process_query_result(self, query_result: dict[str, typing.Any]) -> None:
        report_data = wcl.ReportData(**query_result)

        for fight in report_data.report.fights:
            if fight.id not in [self.fight.fight_id, -1]:
                continue

            if fight.phaseTransitions:
                self.fight.phases = []
                for phase_transition in fight.phaseTransitions:
                    ts = phase_transition.startTime - self.fight.start_time_rel
                    if ts <= 100:  # skip pull as phase
                        continue
                    self.fight.add_phase(ts=ts)

    def needs_load(self) -> bool:
        if self.fight.phases:
            return False
        if not (boss := self.fight.boss):
            return False
        if not (raid_boss := boss.raid_boss):
            return False
        return raid_boss.phase_type == raid_boss.PhaseType.DYNAMIC
