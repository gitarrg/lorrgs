"""0: 


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/DzLQG1Rkp4xtdJgh?fight=16"

"""

from lorgs.models.raid_boss import RaidBoss
from lorgs.data.classes import *


LOOMITHAR = RaidBoss(
    id=3131,
    name="Loom'ithar",
    nick="Loom'ithar",
    icon="inv_112_achievement_raid_silkworm.jpg",
)
boss = LOOMITHAR


################################################################################
# Trinkets
