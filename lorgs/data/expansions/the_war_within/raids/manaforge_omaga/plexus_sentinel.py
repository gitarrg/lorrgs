"""01: Plexus Sentinel


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/DzLQG1Rkp4xtdJgh?fight=16"

"""

from lorgs.models.raid_boss import RaidBoss
from lorgs.data.classes import *


PLEXUS_SENTINEL = RaidBoss(
    id=3129,
    name="Plexus Sentinel",
    nick="Plexus Sentinel",
    icon="inv_112_achievement_raid_automaton.jpg",
)
boss = PLEXUS_SENTINEL
