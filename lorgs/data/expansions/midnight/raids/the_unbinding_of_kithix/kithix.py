"""Kith'ix (The Unbinding of Kith'ix).

https://www.warcraftlogs.com/reports/Dx4Y7r6H2kdtXRJw?fight=130

"""

from lorgs.data.retail.classes import *
from lorgs.models.raid_boss import RaidBoss


KITHIX = RaidBoss(
    id=3513,
    name="Kith'ix",
    nick="Kith'ix",
    icon="8214194.jpg",
)
boss = KITHIX


################################################################################
# Spells

################################
# Stage One: Darkness' Domain

# Summon Adds
boss.add_buff(
    spell_id=1301511,
    name="Voidswarm",
    duration=6,
    color="rgb(212, 114, 255)",
    icon="spell_shadow_shadesofdarkness.jpg",
)
# Kith'ix tears open void portals over 6 sec,
# inflicting Shadow damage every 2 sec and summoning aqir servants.


# Raid AOE (100 Energy)
boss.add_cast(
    spell_id=1302951,
    name="Suffocating Darkness",
    duration=44,  # damage window until Liadrin's Divine Radiance
    color="rgb(237, 36, 69)",
    icon="inv_112_raidtrinkets_blobofswirlingvoid_gold.jpg",
)
# 5 sec cast
# A swirling storm of darkness inflicts Shadow damage to all players every 1 sec
# as it closes in around them.


boss.add_cast(
    spell_id=1304424,
    name="Extinguish",
    duration=8,
    color="rgb(88, 17, 242)",
    icon="inv_elemental_primal_shadow.jpg",
)
# 8 sec cast
# A devastating shockwave inflicts heavy Shadow damage to all players and removes Light's Embrace.


boss.add_debuff(
    spell_id=1303406,
    name="Abyssal Grasp",
    duration=8,
    show=False,
    color="rgb(86, 40, 160)",
    icon="spell_priest_voidtendrils.jpg",
)
# Void tendrils grab random players, absorbing incoming healing.
# After 8 sec, players this effect is not removed from are dragged into the darkness.


boss.add_debuff(
    spell_id=1304045,
    name="Unspeakable Horrors",
    duration=6,
    show=False,
    color="rgb(235, 77, 161)",
    icon="spell_misc_emotionafraid.jpg",
)
# Random players are feared for 6 sec, then succumb to Overwhelming Fear:
# a scream that inflicts Shadow damage to all players, reduced based on distance.


################################
# Stage Two: Last Light

# 25% HP: Stage 2 start
# boss.add_debuff(
#     spell_id=1301110,
#     name="Stygian Howl",
#     duration=6.8,
#     color="rgb(166, 139, 161)",
#     icon="ability_warlock_eradication.jpg",
# )
# Kith'ix howls with otherworldly fury, stunning all players.
# He then absorbs all of his minions and abilities and begins casting Eightfold Eclipse.


# boss.add_cast(
#     spell_id=1301479,
#     name="Eightfold Eclipse",
#     duration=4,
#     color="rgb(57, 15, 184)",
#     icon="inv_nullstone_void.jpg",
# )
# 4 sec cast
# Eclipses inflict Shadow damage to all players.
# Once the final eclipse is manifest, they converge upon Lady Liadrin, killing all players.
