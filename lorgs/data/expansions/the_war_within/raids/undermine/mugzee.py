"""07: Mug'Zee, Heads of Security

PTR Logs:

    All Reports
        https://www.warcraftlogs.com/zone/reports?zone=42&boss=3015

    Normal
        Consequence:
        https://www.warcraftlogs.com/reports/kMJRrNVK4gLhd87T?fight=53

    Mythic
        Northern Sky:
        https://www.warcraftlogs.com/reports/9FCGxtgrqwM1h2AH?fight=36

"""

from lorgs.models.raid_boss import RaidBoss


MUGZEE = RaidBoss(
    id=3015,
    name="Mug'Zee, Heads of Security",
    nick="Mug'Zee",
    icon="inv_111_raid_achievement_mugzeeheadsofsecurity.jpg",
)
boss = MUGZEE


################################################################################
# Trinkets

MUGS_MOXIE_JUG = MUGZEE.add_trinket(
    spell_id=0,
    name="Mug's Moxie Jug",
    icon="inv_111_blackbloodfueledcontainer.jpg",
    item=230192,
)
"""int main + crit proc

> Equip: Your spells have a chance to send you into a frenzy, granting you
> 742 Critical Strike for 15 sec. While frenzied, each spell cast grants an
> additional 742 Critical Strike but does not refresh the duration.
> This effect may only occur every 1 sec.
"""


ZEES_THUG_HOTLINE = MUGZEE.add_trinket(
    spell_id=0,
    name="Zee's Thug Hotline",
    icon="inv_111_remotecontrol_gallywix.jpg",
    item=230199,
)
"""agi/str main + dmg proc

> Equip: Your abilities have a chance to call a member of the Goon Squad to
> attack your target for 10 sec. Gaining Bloodlust or a similar effect summons the whole crew.
"""


################################################################################

# Side Swaps
# Casts
# * https://www.wowhead.com/ptr-2/spell=468728/mug-taking-charge
# * https://www.wowhead.com/ptr-2/spell=468794/zee-taking-charge
# Buffs:
# * https://www.wowhead.com/ptr-2/spell=466459/head-honcho-mug
# * https://www.wowhead.com/ptr-2/spell=466460/head-honcho-zee


################################################################################
# Red Side / Mug

# Circles -> Jails on 2 players
boss.add_cast(
    spell_id=472631,
    name="Earthshaker Gaol",
    duration=10,  # todo: check duration
    color="hsl(30, 50%, 60%)",
    icon="inv_elementalearth2.jpg",
)

# Frontal
boss.add_cast(
    spell_id=466509,
    name="Stormfury Finger Gun",
    duration=3 + 4,
    icon="spell_shaman_crashlightning.jpg",
    color="hsl(220, 60%, 60%)",
    show=False,
)

# Ice Arrows --> Break Walls (heroic)
boss.add_cast(
    spell_id=466470,
    name="Frostshatter Boots",
    duration=2,
    icon="spell_hunter_icetrap.jpg",
    color="hsl(180, 80%, 70%)",
    show=False,
)

# Tank Hit: Molten Gold Knuckles
boss.add_cast(
    spell_id=467201,
    name="Molten Gold Knuckles",
    duration=2.5,
    cooldown=10,  # estimate duration. depends on tank movement
    icon="inv_legendary_fistweapon.jpg",
    color="hsl(220, 80%, 70%)",
    show=False,
)


################################################################################
# Blue Side / Zee


# trigger on side swap (Red -> Blue)
boss.add_cast(
    spell_id=423265,
    name="Uncontrolled Destruction",
    duration=6,
    color="hsl(120, 50%, 50%)",
    icon="ability_siege_engineer_detonate.jpg",
)


# spawns Mines next to players
boss.add_cast(
    spell_id=466539,
    name="Unstable Crawler Mines",
    duration=1.5 + 2,  # Cast is 1.5sec but Buff on Boss is 3.5
    color="hsl(0, 50%, 50%)",
    icon="inv_misc_bomb_02.jpg",
)


# Group Soak
# applies Radiation Sickness (469076) -> only soak once per 60sec
boss.add_cast(
    spell_id=467379,
    name="Goblin-guided Rocket",
    duration=2 + 8,
    color="hsl(20, 50%, 50%)",
    icon="ability_mount_rocketmount.jpg",
)


# Big Frontal on random player
boss.add_cast(
    spell_id=466545,
    name="Spray and Pray",
    duration=3.5 + 3,
    color="hsl(45, 75%, 50%)",
    icon="ability_hunter_markedshot.jpg",
)

# Line to random person -> Tank needs to soak
boss.add_cast(
    spell_id=1223085,
    name="Double Whammy Shot",
    duration=2.5,
    color="hsl(310, 75%, 70%)",
    icon="ability_hunter_burstingshot.jpg",
)

# Big Red Circle around random player
# -> destroys mines
boss.add_cast(
    spell_id=0,  # TODO
    name="Explosive Payload",
    duration=6,
    icon="ability_hunter_explosiveshot.jpg",
    show=False,
    query=False,  # until spell ID is found
)


# Adds: Channel on Random Player (kick/stun?)
boss.add_cast(
    spell_id=1215488,
    name="Disintegration Beam",
    duration=12,
    icon="ability_siege_engineer_purification_beam.jpg",
    show=False,
)

################################################################################
# Phases

# Head Honcho: Mug
boss.add_phase(name="Mug {:d}", spell_id=466459, event_type="applybuff")

# Head Honcho: Zee
boss.add_phase(name="Zee {:d}", spell_id=466460, event_type="applybuff")

# Head Honcho: Mug'Zee
boss.add_phase(name="P2", spell_id=1222408, event_type="applybuff")
