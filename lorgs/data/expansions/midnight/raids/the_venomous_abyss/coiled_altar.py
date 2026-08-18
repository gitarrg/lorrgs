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

################################
# Stage One: Serpent's Bargain

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


# Mythic: spawn Coalesced Venom
boss.add_cast(
    spell_id=1299960,
    name="Toxic Deluge",
    duration=3,
    color="rgb(177, 57, 237)",
    icon="spell_shadow_plaguecloud.jpg",
)
# The crucible spews chunks of coagulated poison around the arena.
# Each missile creates a Coalesced Venom.


# Group Soak
boss.add_cast(
    spell_id=1283489,
    name="Guillotine",
    duration=5,
    color="rgb(207, 34, 14)",
    icon="warrior_talent_icon_mastercleaver.jpg",
)
# Zul'jan throws his axe at a player, inflicting Physical damage
# split evenly among players within 9 yards of the target.
# The axe then swells with poison before erupting with a Widow's Kiss.
#
# If Guillotine fails to hit at least 5 players, the axe instead inflicts an Execution.


boss.add_cast(
    spell_id=1283623,
    name="Widow's Kiss",
    duration=6,
    color="rgb(250, 192, 177)",
    icon="spell_shadow_soothingkiss.jpg",
)
# The Axe erupts in a violent plume that scatters a deadly toxin.


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


################################
# Stage Two: Usurper's Reprisal

boss.add_cast(
    spell_id=1286918,
    name="Eternal Nightfall",
    duration=15,
    color="rgb(230, 18, 54)",
    icon="spell_shadow_twilight.jpg",
)
# Malacrass surrounds himself in a Veil of Twilight, preparing a devastating attack.
# Interruptible if the shield is broken.


boss.add_cast(
    spell_id=1285643,
    name="Dreadmarch",
    duration=5,
    color="rgb(196, 33, 150)",
    icon="spell_nzinsanity_fearofdeath.jpg",
)
# Malacrass sends shadowy tendrils into players and possesses them.
# When broken, Manifestations of Dread emerge.


# Summon Adds
boss.add_cast(
    spell_id=1286441,
    name="Spiritcackle",
    duration=3,
    color="rgb(182, 178, 217)",
    icon="spell_shadow_deathsembrace.jpg",
)
# Malacrass calls upon spirits to manifest a Spiteful Soulcoiler.


boss.add_cast(
    spell_id=1286895,
    name="Gloombomb",
    duration=5,
    color="rgb(130, 67, 181)",
    icon="spell_shadow_shadowfury.jpg",
)
# Malacrass infuses players with shadow. Upon expiration they explode,
# inflicting Shadow damage to players within 15 yards.


# Tank Hit
boss.add_cast(
    spell_id=1286620,
    name="Soul Sever",
    duration=4,
    color="rgb(114, 173, 160)",
    icon="ability_demonhunter_soulcleave2.jpg",
    show=False,
)
# Malacrass blasts shadow energy at his primary target in a frontal cone.
# Players hit are afflicted with Gravebound. Destroys Manifestations of Dread.


################################
# Intermission: The Claimed Vessel

boss.add_cast(
    spell_id=1304032,
    name="Soulbinding",
    duration=35,
    color="rgb(18, 120, 89)",
    icon="spell_necro_deathall.jpg",
)
# Malacrass begins a ritual to bind his soul to Zul'jan.
# Zul'jan takes 100% increased damage during Ghastly Regeneration.


################################
# Stage Three: Coiled Union

boss.add_cast(
    spell_id=1298381,
    name="Defilement of the Coiled Altar",
    duration=8,
    color="rgb(237, 43, 150)",
    icon="ability_warlock_shadowflame.jpg",
)
# Zul'jan defiles the power of Ula'tek and infuses himself with shadow for 8 sec.


boss.add_cast(
    spell_id=1299267,
    name="Grim Guillotine",
    duration=3.5,
    color="rgb(73, 230, 167)",
    icon="inv_polearm_2h_mawnecromancerboss_d_01_darkblue.jpg",
)


# Tank Hit
boss.add_cast(
    spell_id=1307292,
    name="Blighted Sever",
    duration=3,
    color="rgb(174, 201, 141)",
    icon="ability_creature_felsunder.jpg",
    show=False,
)
