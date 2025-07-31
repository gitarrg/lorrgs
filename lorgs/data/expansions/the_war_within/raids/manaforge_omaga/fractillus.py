"""0: 


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/DzLQG1Rkp4xtdJgh?fight=16"

"""

from lorgs.models.raid_boss import RaidBoss
from lorgs.data.classes import *


FRACTILLUS = RaidBoss(
    id=3133,
    name="Fractillus",
    nick="Fractillus",
    icon="inv_112_achievement_raid_glasselemental.jpg",
)
boss = FRACTILLUS


################################################################################
# Trinkets
