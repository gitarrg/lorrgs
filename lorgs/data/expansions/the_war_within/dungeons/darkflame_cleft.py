# IMPORT LOCAL LIBRARIES
from lorgs.data.retail.classes import *
from lorgs.models.dungeon import Dungeon
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Trinkets


BURIN_OF_THE_CANDLE_KING = WowTrinket(
    spell_id=443529,
    cooldown=90,
    name="Burin of the Candle King",
    icon="inv_jewelcrafting_70_jeweledlockpick.jpg",
    item=219306,
)
"""On-Use Absorb

probably worth tracking some sort of buff, in case this gets played

> Use: Carve a wax copy of your target, which absorbs 50% of their damage taken.
> The absorption heats up the wax, causing it to melt after absorbing 264398 damage. (1 Min, 30 Sec Cooldown)

"""

CARVED_BLAZIKON_WAX = "[Carved Blazikon Wax]"
"""Vers Proc (15sec)

> Equip: Your spells have a chance to imbue the wax, causing it to form into a
> blazing candle for 15 sec which increases your Versatility by 1292, further
> increased by 136 while you remain within its light.
"""

CONDUCTORS_WAX_WHISTLE = "[Conductor's Wax Whistle]"
"""Random Damage Proc

> Equip: Your attacks have a chance to direct a Kobold Cart towards your target,
> sending a careening troop that collides with enemies, inflicting 50842 Physical
> damage split between enemies impacted.
"""

REMNANT_OF_DARKNESS = "[Remnant of Darkness]"
"""Accumulates stacks -> aoe damage split

> Equip: Your abilities have a chance to call the Darkness to you,
> increasing your <Primary Stat> by 245, up to 1225.
> Upon reaching full power, the Darkness is unleashed, inflicting 99665 Shadow damage
> split between nearby enemies over 15 sec before fading back into the remnant.
"""


################################################################################

DARKFLAME_CLEFT = Dungeon(name="Darkflame Cleft")
