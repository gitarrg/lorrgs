# IMPORT LOCAL LIBRARIES
from lorgs.data.retail.classes import *
from lorgs.models.dungeon import Dungeon
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Trinkets

CHARGED_STORMROOK_PLUME = WowTrinket(
    spell_id=443337,
    cooldown=90,
    name="Charged Stormrook Plume",
    icon="inv_achievement_dungeon_rookery.jpg",
    item=219294,
)
"""1sec cast -> charge to location + split damage

460469 = trigger
443337 = release

> Use: Hold out the feather for 11 sec to strike with the power of the storm,
> crashing down on the target location and inflicting 104053 Nature damage split
> between nearby enemies. (1 Min, 30 Sec Cooldown)
"""


ENTROPIC_SKARDYN_CORE = "[Entropic Skardyn Core]"
"""Random Int Proc

> Equip: Your spells have a chance to destabilize the void energy, releasing a corrupted fragment.
> Retrieving a fragment briefly infuses you with its power, increasing your Intellect by 1235 for 15 sec.

"""

SIGIL_OF_ALGARI_CONCORDANCE = "[Sigil of Algari Concordance]"
"""Random Pet Proc

> Equip: Your abilities have a chance to call an earthen ally to your aid, supporting you in combat. (15s cooldown)
"""

################################################################################


THE_ROOKERY = Dungeon(name="The Rookery")
