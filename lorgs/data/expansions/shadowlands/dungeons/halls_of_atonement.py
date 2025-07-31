# IMPORT LOCAL LIBRARIES
from lorgs.data.classes import *
from lorgs.models.dungeon import Dungeon
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Trinkets

CURSED_STONE_IDOL = WowTrinket(
    spell_id=246344,
    name="Cursed Stone Idol",
    icon="inv_qirajidol_onyx.jpg",
    cooldown=90,
    item=246344,
)
"""DMG + Crit

> Use: Channel for 1 sec to invoke the wrath of the idol, increasing your
> Critical Strike by 5143 for 15 sec. The force slams the earth, dealing 65564
> Nature damage to all nearby enemies and increasing Critical Strike by 265 per enemy hit,
> up to a maximum of 6000. (1 Min, 30 Sec Cooldown)
"""
# CURSED_STONE_IDOL.add_specs(*AGI_SPECS)
# CURSED_STONE_IDOL.add_specs(*STR_SPECS)


SUNBLOOD_AMETHYST = WowTrinket(
    spell_id=343393,
    name="Sunblood Amethyst",
    icon="inv_jewelcrafting_nightseye_01.jpg",
    cooldown=90,
    duration=15,
    item=178826,
)
"""DMG + int zone

> Use: Tear the anima from your target dealing 2748 Shadow damage and
> forming a font of power at your feet, increasing your Intellect by 31 for 15 sec
> while you stand within it. (1 Min, 30 Sec Cooldown)
"""
# SUNBLOOD_AMETHYST.add_specs(*INT_SPECS)


################################################################################

HALLS_OF_ATONEMENT = Dungeon(
    name="Halls of Atonement",
    trinkets=[
        CURSED_STONE_IDOL,
        SUNBLOOD_AMETHYST,
    ],
)
