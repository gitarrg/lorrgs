"""All Playable Classes in the Game."""
from __future__ import annotations

from lorgs.data.classes.deathknight import *
from lorgs.data.classes.demonhunter import *
from lorgs.data.classes.druid import *
from lorgs.data.classes.evoker import *
from lorgs.data.classes.hunter import *
from lorgs.data.classes.mage import *
from lorgs.data.classes.monk import *
from lorgs.data.classes.other import *
from lorgs.data.classes.paladin import *
from lorgs.data.classes.priest import *
from lorgs.data.classes.rogue import *
from lorgs.data.classes.shaman import *
from lorgs.data.classes.warlock import *
from lorgs.data.classes.warrior import *


# a few collections used to assign trinkets and consumables
# fmt: off
ALL_SPECS = TANK.specs | HEAL.specs | MDPS.specs | RDPS.specs
DPS_SPECS = MDPS.specs | RDPS.specs

INT_SPECS = {*HEAL.specs, *MAGE.specs, *WARLOCK.specs, PRIEST_SHADOW, SHAMAN_ELEMENTAL, DRUID_BALANCE, EVOKER_DEVASTATION, EVOKER_AUGMENTATION, DEMONHUNTER_DEVOURER}
AGI_SPECS = {*HUNTER.specs, *ROGUE.specs, *DEMONHUNTER.specs, SHAMAN_ENHANCEMENT, MONK_BREWMASTER, MONK_WINDWALKER, DRUID_FERAL}
STR_SPECS = {*WARRIOR.specs, *DEATHKNIGHT.specs, PALADIN_PROTECTION, PALADIN_RETRIBUTION}

INT_DPS_SPECS = INT_SPECS - HEAL.specs
AGI_DPS_SPECS = AGI_SPECS - TANK.specs
STR_DPS_SPECS = STR_SPECS - TANK.specs
