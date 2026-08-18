"""The Coiled Altar (The Venomous Abyss).

NS:
https://www.warcraftlogs.com/reports/pfkrcn7xPdDL1jqH?fight=45

"""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss


COILED_ALTAR = RaidBoss(
    id=3429,
    name="The Coiled Altar",
    nick="Coiled Altar",
    icon="inv_121_raid_achievement_zuljinmalacrass.jpg",
)
boss = COILED_ALTAR


################################################################################
# Trinkets


################################################################################
# Spells

# Group Soak
boss.add_cast(
    spell_id=1283489,
    name="Guillotine",
    duration=3.5,
    color="rgb(207, 34, 14)",
    icon="warrior_talent_icon_mastercleaver.jpg",
)
# Zul'jan throws his axe at a player, inflicting 5417143 Physical damage
# split evenly among players within 9 yards of the target and increasing
# their damage taken from Guillotine by 500% for 1.7 min.
# This effect ignores armor. The axe then swells with poison before erupting with a Widow's Kiss.
#
# If Guillotine fails to hit at least 5 players, the axe instead inflicts an Execution.


# Summon Axe
boss.add_cast(
    spell_id=1283832,
    name="Axegrinder",
    duration=3,
    color="rgb(222, 167, 64)",
    icon="ability_warrior_bladestorm.jpg",
)
# Zul'jan hurls out axes that inflict 583498 Physical damage to players within
# 4 yards of each impact point, knocking them away.
# The axes wander the arena for 3 min, inflicting 104176 Physical damage every
# 0.25 sec to players within 0 yards. This effect ignores armor.


# 8 sec AOE
boss.add_cast(
    spell_id=1282487,
    name="Fangs of the Coiled Altar",
    duration=8,
    color="rgb(70, 227, 73)",
    icon="spell_nature_poisoncleansingtotem.jpg",
)
# Zul'jan channels the power of The Coiled Altar, inflicting 83341 Nature damage
# to all players and gaining 3 applications of Twinfang Toxin every 1 sec for 8 sec.
#
# The mouths of The Coiled Altar overflow, spewing Noxious Ground beneath them
# that quickly swell and slowly subside over time.


boss.add_cast(
    spell_id=1306906,
    name="Venomfang",
    duration=2,
    cooldown=14,
    color="rgb(93, 166, 48)",
    icon="ability_rogue_poisonedknife.jpg",
)
# Zul'jan hurls a poison-coated axe between multiple players, inflicting 125011
# Nature damage every 2 sec for 14 sec.


# Tank Hit
boss.add_cast(
    spell_id=1299684,
    name="Sever",
    duration=3,
    color="rgb(184, 63, 29)",
    icon="ability_criticalstrike.jpg",
    show=False,
)
# Zul'jan unleashes a mighty cleave at his current target, inflicting 3333627 Physical damage
# to players in a frontal cone and increasing their damage taken from Sever by 200% for 30 sec.
#
# Destroys Coalesced Venoms and Virulent Mutations.
