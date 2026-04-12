from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import datetime
import textwrap
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.clients import wcl
from lorgs.logger import logger
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.warcraftlogs_boss import Boss
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_player import Player
from lorgs.models.warcraftlogs_report import Report
from lorgs.models.wow_class import WowClass

from .base_loader import BaseLoader


class FightLoader(BaseLoader):
    """wip"""

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
