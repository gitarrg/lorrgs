"""02: Soulbinder Naazindhri 


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/DzLQG1Rkp4xtdJgh?fight=16"

"""

from lorgs.models.raid_boss import RaidBoss
from lorgs.data.classes import *


NAAZINDHRI = RaidBoss(
    id=3130,
    name="Soulbinder Naazindhri",
    nick="Naazindhri",
    icon="inv_112_achievement_raid_binder.jpg",
)
boss = NAAZINDHRI


################################################################################
# Trinkets
