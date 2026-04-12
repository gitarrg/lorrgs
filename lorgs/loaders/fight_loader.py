from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import datetime
import textwrap
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.clients import wcl
from lorgs.loaders.fight_phases import FightPhasesLoader
from lorgs.logger import logger
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.warcraftlogs_boss import Boss
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_player import Player
from lorgs.models.wow_spec import WowSpec

from .base_loader import BaseLoader


if typing.TYPE_CHECKING:
    from lorgs.models.warcraftlogs_report import Report


def player_from_composition_data(composition_data: wcl.CompositionEntry) -> Player | None:
    # Get Class and Spec
    if not composition_data.specs:
        logger.warning("Player has no spec: %s", composition_data.name)
        return None

    spec_data = composition_data.specs[0]
    spec_name = spec_data.spec
    class_name = composition_data.type
    spec = WowSpec.get(name_slug_cap=spec_name, wow_class__name_slug_cap=class_name)
    if not spec:
        logger.warning("Unknown Spec: %s", spec_name)
        return None

    # create and return yield player object
    return Player(
        source_id=composition_data.id,
        name=composition_data.name,
        class_slug=spec.wow_class.name_slug,
        spec_slug=spec.full_name_slug,
    )


class FightLoader(BaseLoader):

    def __init__(self, fight: Fight) -> None:
        self.fight = fight

    def needs_load(self) -> bool:
        return not self.fight.players

    @staticmethod
    def fight_from_wcl_fight(fight_data: wcl.ReportFight, report: Report) -> Fight | None:
        """Create a Fight from a WCL Fight."""
        # skip trash fights
        if not fight_data.encounterID:
            return None

        try:
            difficulty = RaidDifficulty(fight_data.difficulty)
        except ValueError:
            return None

        fight = Fight(
            fight_id=fight_data.id,
            percent=fight_data.fightPercentage,
            kill=fight_data.kill,
            start_time=report.start_time + datetime.timedelta(milliseconds=fight_data.startTime),
            duration=fight_data.endTime - fight_data.startTime + 1,  # somehow there is 1ms missing
            difficulty=difficulty,
        )

        # Fight: Boss
        if raid_boss := RaidBoss.get(id=fight_data.encounterID):
            fight.boss = Boss.from_raid_boss(raid_boss)
            fight.boss.fight = fight

        # Fight: Phases
        for phase_transition in fight_data.phaseTransitions:
            ts = phase_transition.startTime - fight_data.startTime
            if ts <= 0:  # skip pull as phase
                continue
            fight.add_phase(ts=ts)

        return fight

    def get_query(self) -> str:
        if not self.fight.report:
            raise ValueError("Missing Parent Report")

        return textwrap.dedent(
            f"""\
            reportData
            {{
                report(code: "{self.fight.report.report_id}")
                {{
                    summary: table(fightIDs: {self.fight.fight_id}, dataType: Summary)

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

    def _process_summary(self, summary: wcl.ReportSummary) -> None:
        self.fight.duration = self.fight.duration or summary.totalTime

        total_damage = summary.damageDone
        total_healing = summary.healingDone

        self.fight.players = []
        for composition_data in summary.composition:

            player = player_from_composition_data(composition_data)
            if not player:
                continue

            # Get Total Damage or Healing
            total_data = total_healing if player.spec.role.code == "heal" else total_damage
            for data in total_data:
                if data.id == composition_data.id:
                    player.total = data.total // (self.fight.duration / 1000)
                    break

            player.fight = self.fight
            player.process_death_events(summary.deathEvents)
            self.fight.players.append(player)

        self.fight.players.sort(key=lambda player: (player.spec.role, player.spec, player.name))

    def process_query_result(self, query_result: dict[str, typing.Any]) -> None:
        report_data = wcl.ReportData(**query_result)

        if summary := report_data.report.summary:
            self._process_summary(summary)

        phase_loader = FightPhasesLoader(fight=self.fight)
        if phase_loader.needs_load():
            phase_loader.process_query_result(query_result)
