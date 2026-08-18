"""Ula'tek (The Venomous Abyss).

https://www.warcraftlogs.com/reports/2Xg3AQYFzLt7r1hN?fight=30

"""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss


ULATEK = RaidBoss(
    id=3492,
    name="Ula'tek",
    nick="Ula'tek",
    icon="inv_121_raid_achievement_ulatek.jpg",
)
boss = ULATEK


################################################################################
# Trinkets


################################################################################
# Spells

################################
# Stage One: Fury of the Serpent Mother

boss.add_cast(
    spell_id=1311807,
    name="Caustic Waves",
    duration=6,
    color="rgb(136, 227, 79)",
    icon="inv_ability_poison_wave.jpg",
)
# Ula'tek sends waves of venom across the platform.
# Waves that connect with Devourer's Spawn cause the eggs to instantly hatch.


# Summon Adds
boss.add_cast(
    spell_id=1304012,
    name="Call of the Serpent",
    duration=4,
    color="rgb(93, 166, 48)",
    icon="8125100.jpg",
)
# Ula'tek roars, causing her spawn to fall from the ceiling.


# Group Soak
boss.add_cast(
    spell_id=1308927,
    name="Spectral Coils",
    duration=12,
    color="rgb(182, 178, 217)",
    icon="spell_animamaldraxxus_nova.jpg",
)
# Spectral Coils crush anything beneath them.
# Damage is reduced by the number of players within 10 yards of the impact.


boss.add_cast(
    spell_id=1296301,
    name="Mephitic Thrash",
    duration=4,
    color="rgb(130, 135, 80)",
    icon="ability_creature_poison_04.jpg",
)
# Ula'tek's tail sweeps the ground, knocking players back and applying a DoT.


# Tank
boss.add_cast(
    spell_id=1298367,
    name="Mother's Wrath",
    duration=5,
    color="rgb(227, 18, 91)",
    icon="inv_misc_monsterfang_02.jpg",
    show=False,
)
# Ula'tek knocks back her current target, marking them for wrath.
# If her current target is outside her reach, effects hit all players.


# Burn Window
boss.add_cast(
    spell_id=1286860,
    name="Rage of the Shackled",
    duration=20,
    color="rgb(237, 19, 48)",
    icon="inv_121_raid_achievement_ulatek.jpg",
)
# Ula'tek rages for 20 sec, raining Falling Debris and exposing her Venomous Heart.


boss.add_buff(
    spell_id=1299526,
    name="Venomous Heart",
    duration=20,
    color="rgb(247, 164, 47)",
    icon="inv_121_trinket_raid_ulatek_heart.jpg",
)
# The beating core of Ula'tek. All damage taken is increased by 100% for 20 sec.


################################
# Stage Two: Children of the Doomscale

boss.add_cast(
    spell_id=1301213,
    name="Shadow Molt",
    duration=3,
    color="rgb(114, 20, 168)",
    icon="spell_warlock_demonsoul.jpg",
)
# The Doomscale Warden sheds its shadow skin and slithers to a new destination.


boss.add_cast(
    spell_id=1302950,
    name="Writhing Gestation",
    duration=3,
    color="rgb(68, 133, 16)",
    icon="rogue_leeching_poison.jpg",
    variations=[1290990],
)
# The Doomscale Warden transforms nearby Devourer's Spawn into a Slithering Clutch
# that hatches after 20 sec.


boss.add_cast(
    spell_id=1301117,
    name="Grasping Fangs",
    duration=2,
    color="rgb(160, 173, 132)",
    icon="inv_121_trinket_raid_ulatek_ulatekclaw.jpg",
)
# The Doomscale Warden sinks fangs into random players, rooting them until broken.


boss.add_buff(
    spell_id=1303410,
    name="Defect: Weakened",
    duration=0,
    color="rgb(73, 230, 167)",
    icon="ability_deathknight_heartstopaura.jpg",
)
# Disrupting the Ravenous Doomscale's gestation weakens it,
# increasing all its damage taken by 100%.
