"""0: 


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/DzLQG1Rkp4xtdJgh?fight=16"

"""

from lorgs.models.raid_boss import RaidBoss
from lorgs.data.classes import *


ARAZ = RaidBoss(
    id=3132,
    name="Forgeweaver Araz",
    nick="Araz",
    icon="inv_112_achievement_raid_engineer.jpg",
)
boss = ARAZ


################################################################################
# Trinkets
