"""0: 


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/DzLQG1Rkp4xtdJgh?fight=16"

"""

from lorgs.models.raid_boss import RaidBoss
from lorgs.data.classes import *


SALHADAAR = RaidBoss(
    id=3134,
    name="Nexus-King Salhadaar",
    nick="Salhadaar",
    icon="inv_112_achievement_raid_salhadaar.jpg",
)
boss = SALHADAAR


################################################################################
# Trinkets
