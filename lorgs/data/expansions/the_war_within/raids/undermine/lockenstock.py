"""05: Sprocketmonger Lockenstock

PTR Logs:
    Mythic / Northern Sky
    https://www.warcraftlogs.com/reports/YxpKjwFbkrC4VGv3?fight=61


"""

from lorgs.models.raid_boss import RaidBoss


LOCKENSTOCK = RaidBoss(
    id=3013,
    name="Sprocketmonger Lockenstock",
    nick="Lockenstock",
    icon="inv_111_raid_achievement_sprocketmongerlocknstock.jpg",
)
boss = LOCKENSTOCK


################################################################################
# Trinkets

MISTER_LOCK_N_STALK = boss.add_trinket(
    spell_id=0,
    cooldown=20,
    name="Mister Lock-N-Stalk",
    icon="inv_111_healraydrone_gallywix.jpg",
    item=230193,
)
"""Random DMG Proc. Can swap between AoE or ST.

Precision Blasting
> Your spells and abilities have a high chance to lase your target for Precision Blasting,
> calling in Mister Lock-N-Stalk to deal 3555 Physical damage to your target.
> https://www.wowhead.com/ptr-2/spell=467492/precision-blasting

Mass Destruction
> Your spells and abilities have a high chance to lase enemies for Mass Destruction,
> calling in Mister Lock-N-Stalk to deal 2074 Fire damage split between your target and nearby enemies.
> https://www.wowhead.com/ptr-2/spell=467497/mass-destruction

"""
# MISTER_LOCK_N_STALK.add_specs(*DPS_SPECS)


MISTER_PICK_ME_UP = boss.add_trinket(
    spell_id=0,
    name="Mister Pick-Me-Up",
    icon="inv_111_healraydrone_bilgewater.jpg",
    item=230186,
)
"""random healing proc

> Your healing spells and abilities have a chance to summon Mister Pick-Me-Up for 6 sec,
> firing a healing beam every 2 sec that jumps between 5 injured allies to restore 72074 health each.
>
> Overhealing from this effect irradiates allies to deal Nature damage to nearby
> enemies over 1.5 sec, increased by additional overhealing.
"""


################################################################################

# raid wide AoE
boss.add_cast(
    spell_id=465232,
    name="Sonic Ba-Boom",
    duration=2,
    cooldown=10,
    color="hsl(0, 50%, 50%)",
    icon="inv_sonic_debuff.jpg",
)


# Mine spawn / Foot Blasters
# trigger them to explode 1 by 1
# TODO: track triggering
boss.add_cast(
    spell_id=1217231,
    name="Foot-Blasters",
    duration=1.5,
    color="hsl(50, 60%, 50%)",
    icon="inv_10_engineering2_boxofbombs_friendly_color1.jpg",
)


# Zone activation --> move to other side
boss.add_cast(
    spell_id=1218418,
    name="Wire Transfer",
    duration=2,
    color="hsl(210, 50%, 50%)",
    icon="inv_10_engineering_manufacturedparts_electricalparts_color1.jpg",
)


# Drills spawn
boss.add_cast(
    spell_id=1216508,
    name="Screw Up",
    duration=2,
    cooldown=4.5,
    color="hsl(30, 60%, 50%)",
    icon="ability_siege_engineer_sockwave_missile.jpg",
    show=False,
)


# Weapons
boss.add_cast(
    spell_id=465232,
    name="Activate Inventions!",
    duration=1,
    color="hsl(260, 50%, 50%)",
    icon="inv_10_engineering_device_gadget1_color2.jpg",
)

# Rockets
boss.add_cast(
    spell_id=1214872,
    name="Pyro Party Pack",
    duration=1.5,
    color="hsl(280, 60%, 60%)",
    icon="inv_summerfest_groundflower.jpg",
)


# Mythic: Debuffs
boss.add_cast(
    spell_id=1217355,
    name="Polarization Generator",
    duration=4,
    color="hsl(320, 70%, 60%)",
    icon="inv_engineering_90_electrifiedether.jpg",
    show=False,
)

# red lasers


##############
# Intermission / Bleeding Edge
boss.add_cast(
    spell_id=466860,
    name="Bleeding Edge",
    duration=20,
    color="hsl(120, 70%, 50%)",
    icon="spell_yorsahj_bloodboil_purple.jpg",
)


################################################################################
# Phases

# Beta Launch
boss.add_phase(name="P2 ({count})", spell_id=1218318, event_type="applybuff")
boss.add_phase(name="P1 ({count})", spell_id=1218318, event_type="removebuff")
