"""All Playable Classes in the Game."""
from __future__ import annotations

from lorgs.data.retail.classes.deathknight import *
from lorgs.data.retail.classes.demonhunter import *
from lorgs.data.retail.classes.druid import *
from lorgs.data.retail.classes.evoker import *
from lorgs.data.retail.classes.hunter import *
from lorgs.data.retail.classes.mage import *
from lorgs.data.retail.classes.monk import *
from lorgs.data.retail.classes.other import *
from lorgs.data.retail.classes.paladin import *
from lorgs.data.retail.classes.priest import *
from lorgs.data.retail.classes.rogue import *
from lorgs.data.retail.classes.shaman import *
from lorgs.data.retail.classes.warlock import *
from lorgs.data.retail.classes.warrior import *


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
