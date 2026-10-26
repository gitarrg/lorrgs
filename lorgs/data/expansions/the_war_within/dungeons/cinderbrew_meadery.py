# Cinderbrew Meadery

# IMPORT LOCAL LIBRARIES
from lorgs.data.retail.classes import *
from lorgs.models.dungeon import Dungeon
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Trinkets

CINDERBREW_STEIN = "Cinderbrew Stein"
"""Random Stat Proc

https://www.wowhead.com/item=219297/cinderbrew-stein

> Equip: Occasionally share a drink with allies who assist you in combat,
> granting them 700 of their primary stat for 15 sec and absorbing 19079 damage.
> You take a sip as well, granting 377 <Primary Stat> and absorbing 89032 damage.
>
> When you fall below 50% health, you take an emergency sip. This may only occur once every 1 min.
"""

RAVENOUS_HONEY_BUZZER = WowTrinket(
    spell_id=448904,
    cooldown=90,
    name="Ravenous Honey Buzzer",
    icon="inv_10_engineering_device_gadget1_color1.jpg",
    item=219298,
)
"""15yd Charge + split dmg

> Use: Call in a ravenous ally and ride off into the sunset (or $443387rad1 yds, whichever is closest),
> inflicting 161686 Fire damage split between all enemies you ride through. (1 Min, 30 Sec Cooldown)
"""
RAVENOUS_HONEY_BUZZER.add_specs(*STR_SPECS)
RAVENOUS_HONEY_BUZZER.add_specs(*AGI_SPECS)


SYNERGISTIC_BREWTERIALIZER = "Synergistic Brewterializer"
"""Random DMG Proc

https://www.wowhead.com/item=219299/synergistic-brewterializer

> Equip: Your spells have a chance to charge the device and request a Backfill Barrel
> near your target's location. Damaging the barrel causes it to explode,
> inflicting 84121 Fire damage split between nearby enemies.
"""

################################################################################


CINDERBREW_MEADERY = Dungeon(name="Cinderbrew Meadery")
