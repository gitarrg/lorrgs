# IMPORT LOCAL LIBRARIES
from lorgs.data.retail.classes import *
from lorgs.models.dungeon import Dungeon
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Trinkets


DARKFUSE_MEDICHOPPER = WowTrinket(
    spell_id=1220488,
    cooldown=120,
    duration=15,
    name="Darkfuse Medichopper",
    icon="inv_111_healraydrone_blackwater.jpg",
    item=232542,
)
"""On-Use Absorb + Vers on Target

> Use: Command the Medichopper to attach to your target, absorbing 134943 damage
> and granting them 1196 versatility for 15 sec.
> While attached, your healing spells have a chance to refuel the chopper,
> granting these bonuses to their host again. (2 Min Cooldown)

"""

GIGAZAPS_ZAP_CAP = "[Gigazap's Zap-Cap]"
"""Random Damage Proc

> Equip: Every 6 sec, Zap your target and 1 nearby enemy for 20752 Nature damage.
> Casting 30 spells Turbo-Charges you for 15 sec, doubling the frequency of your Zaps
> and upgrading them into Giga-Zaps, dealing 62256 Nature Damage instead. (750ms cooldown)
"""

IMPROVISED_SEAFORIUM_PACEMAKER = "[Improvised Seaforium Pacemaker]"
"""extendable Crit Buff every 60sec ?

> Equip: Repurpose a Seaforium charge to give your heart a kick, causing your first ability
> every 60 sec to trigger Explosive Adrenaline, granting 2916 Critical Strike for 15 sec.
>
> While exploding, Critical Strikes cause you to blow up again, extending this duration by 1 sec, up to 15 times.
"""

RINGING_RITUAL_MUD = WowTrinket(
    spell_id=1219102,
    cooldown=120,
    duration=10,
    name="Ringing Ritual Mud",
    icon="inv_misc_food_legion_goomolasses_pool.jpg",
    item=232543,
)
"""On-Use Absorb + pulse AoE

> Use: Become Mudborne, absorbing 7088217 damage and pulsing 291125 Nature damage split between nearby enemies over 10 sec.
>
> Periodic damage you take coalesces into pungent mud to feed the ritual, reducing this cooldown by 22 sec. (2 Min Cooldown)
"""

################################################################################

OPERATION_FLOODGATE = Dungeon(name="Operation: Floodgate")
