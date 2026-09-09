"""Models to read in the Data recived from the Warcraflogs API."""

from .character_ranking import (
    CharacterRanking,
    CharacterRankingReportFightData,
    CharacterRankings,
)
from .fight_rankings import FightRankings, FightRankingsFight, FightRankingsItemsReport
from .query import Query
from .report_actor import ReportActor
from .report_data import Report, ReportData
from .report_events import ReportEvent
from .report_fight import PhaseTransition, ReportFight
from .report_master_data import ReportMasterData
from .report_summary import CompositionEntry, DeathEvent, ReportSummary
from .world_data import WorldData


__all__ = [
    "CharacterRanking",
    "CharacterRankingReportFightData",
    "CharacterRankings",
    "CompositionEntry",
    "DeathEvent",
    "FightRankings",
    "FightRankingsFight",
    "FightRankingsItemsReport",
    "PhaseTransition",
    "Query",
    "Report",
    "ReportActor",
    "ReportData",
    "ReportEvent",
    "ReportFight",
    "ReportMasterData",
    "ReportSummary",
    "WorldData",
]
