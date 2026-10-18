"""04: Stix Bunkjunker.

PTR Logs:
    Heroic / Melee Mechanics
    https://www.warcraftlogs.com/reports/jMwdH1rf3XZK7Avp?fight=7

"""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss


STIX = RaidBoss(
    id=3012,
    name="Stix Bunkjunker",
    nick="Stix",
    icon="inv_111_raid_achievement_stixbunkjunker.jpg",
)
boss = STIX

################################################################################
# Trinkets

JUNKMAESTROS_MEGA_MAGNET = boss.add_trinket(
    spell_id=471212,
    duration=6,
    cooldown=20,
    name="Junkmaestro's Mega Magnet",
    icon="inv_111_magnet_gallywix.jpg",
    item=230189,
)
"""Collect stacks -> consume them for on-use dmg

Buff: 1219661

> Equip: Your damaging abilities have a very high chance to charge the magnet, up to 30 times.
> Use: Reverse the magnet's polarity to violently recycle buried garbage,
> dealing 59774 Plague damage to your target per charge.
> Lingering virulence deals 10% of the damage dealt to 5 nearby enemies over 6 sec. (20 Sec Cooldown)
"""
JUNKMAESTROS_MEGA_MAGNET.add_specs(*AGI_SPECS)


SCRAPFIELD_9001 = boss.add_trinket(
    spell_id=466673,
    cooldown=30,
    name="Scrapfield 9001",
    icon="inv_111_forcefieldmodule_steamwheedle.jpg",
    item=230026,
    event_type="buff",
)
"""Shield Proc when below 60% HP. (Tank only)

- Buff: 466673
- Debuff: 472170

> Equip: Falling below 60% health surrounds you with a protective vortex of junk,
> reducing damage taken by 50% for 15 sec or until 996802 damage is prevented.
> This effect may only occur every 30 sec.
> 
> After 20 sec without activating while in combat, the Scrapfield overloads
> to energize you with 2651 Haste for 12 sec.

"""
# SCRAPFIELD_9001.add_specs(*TANK.specs)


################################################################################
# Phase 1:

# Electromagnetic Sorting =
# - tank + random players transform into balls
#   - soak small -> medium -> large trash to grow
# - spawns adds + bombs
boss.add_cast(
    spell_id=464399,
    name="Electromagnetic Sorting",
    duration=1,
    cooldown=5,
    color="hsl(0, 50%, 50%)",
    icon="inv_10_engineering_manufacturedparts_mechanicalparts_color3.jpg",
)


# Incinerator = red spread circles on random players
# https://www.wowhead.com/ptr-2/spell=464149/incinerator
boss.add_cast(
    spell_id=464149,
    name="Incinerator",
    duration=3,
    color="hsl(35, 75%,50%)",
    icon="ability_ironmaidens_bombardment.jpg",
    show=False,
)


# Tank Hit: Demolish
# https://www.wowhead.com/ptr-2/spell=464112/demolish
boss.add_cast(
    spell_id=464112,
    name="Demolish",
    duration=1.25,
    cooldown=50,
    color="#478fb3",
    icon="inv_misc_enggizmos_12.jpg",
    show=False,
)

# Tank Hit: Meltdown
# https://www.wowhead.com/ptr-2/spell=1217954/meltdown'
boss.add_cast(
    spell_id=1217954,
    name="Meltdown",
    duration=1,
    cooldown=3,
    color="##3fbfbd",
    icon="inv_misc_enggizmos_15.jpg",
    show=False,
)


# Intermission
boss.add_cast(
    spell_id=467117,
    name="Overdrive / Trash Compactor",
    duration=10,  # aprox duration
    color="hsl(120, 70%, 50%)",
    icon="spell_nature_unrelentingstorm.jpg",
)
