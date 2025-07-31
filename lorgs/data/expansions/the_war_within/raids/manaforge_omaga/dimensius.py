"""0: 


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/DzLQG1Rkp4xtdJgh?fight=16"

"""

from lorgs.models.raid_boss import RaidBoss
from lorgs.data.classes import *


DIMENSIUS = RaidBoss(
    id=3135,
    name="Dimensius, the All-Devouring",
    nick="Dimensius",
    icon="inv_112_achievement_raid_dimensius.jpg",
)
boss = DIMENSIUS


################################################################################
# Trinkets
