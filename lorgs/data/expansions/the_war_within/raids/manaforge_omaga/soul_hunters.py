"""03: The Soul Hunters 


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/DzLQG1Rkp4xtdJgh?fight=16"

"""

from lorgs.models.raid_boss import RaidBoss
from lorgs.data.classes import *


SOUL_HUNTERS = RaidBoss(
    id=3122,
    name="The Soul Hunters",
    nick="Soul Hunters",
    icon="inv_112_achievement_raid_dhcouncil.jpg",
)
boss = SOUL_HUNTERS


################################################################################
# Trinkets
