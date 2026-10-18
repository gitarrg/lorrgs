"""02: The Amalgamation Chamber"""

from lorgs.models.raid_boss import RaidBoss


AMALGAMATION_CHAMBER = RaidBoss(
    id=2687,
    name="The Amalgamation Chamber",
    icon="inv_achievement_raiddragon_amalgamationchamber.jpg",
)
boss = AMALGAMATION_CHAMBER


################################################################################
# Shadow
#

# run out --> drop circle
boss.add_cast(
    spell_id=405016,
    name="Umbral Detonation",
    duration=2,
    cooldown=6,
    color="#8b47bf",
    icon="spell_shadow_shadowfury.jpg",
)


boss.add_cast(
    spell_id=403459,
    name="Coalescing Void",
    duration=3,
    # cooldown=6, todo: check suck duration
    color="#5b47bf",
    icon="inv_icon_shadowcouncilorb_purple.jpg",
)


# Tank Hit
boss.add_cast(
    spell_id=403699,
    name="Shadow Spike",
    duration=2,
    color="#478fb3",
    icon="ability_ironmaidens_convulsiveshadows.jpg",
    show=False,
)

################################################################################
# Fire
#

# Fire Group Soak
boss.add_cast(
    spell_id=404732,
    name="Fiery Meteor",
    duration=5,
    color="#bf4747",
    icon="spell_mage_meteor.jpg",
)

# Fire Walls
boss.add_cast(
    spell_id=404896,
    name="Swirling Flame",
    duration=2,
    cooldown=5,
    color="#edca2f",
    icon="spell_shaman_lavasurge.jpg",
    show=False,
)

# Soak puddles
boss.add_cast(
    spell_id=404896,
    name="Molten Eruption",
    duration=1,
    color="#ed5f2f",
    icon="ability_rhyolith_volcano.jpg",
    show=False,
)


# Fire Tank Hit
boss.add_cast(
    spell_id=403203,
    name="Flame Slash",
    duration=2,
    color="#478fb3",
    icon="spell_fire_soulburn.jpg",
    show=False,
)


################################################################################
# Phase 2
#

boss.add_cast(
    spell_id=406780,
    name="Phase 2",  # Shadowflame Contamination
    color="#60b336",
    icon="inv_shadowflame_debuff.jpg",
    show=True,
)


# drop circles
# boss.add_cast(
#     spell_id=405641,
#     name="Blistering Twilight",
#     duration=2 + 6,
#     color="#8b47bf",
#     icon="inv_shadowflame_groundstate.jpg",
#     show=False,
# )


# soak puddles
# Molten Eruption (404896) + Umbral Detonation (405016)
boss.add_cast(
    spell_id=408193,
    name="Convergent Eruption",
    duration=1,
    color="#ed5f2f",
    icon="inv_chaos_orb.jpg",
    show=False,
)

# Group Soak
# Fiery Meteor (404732) + Coalescing Void (403459)
boss.add_cast(
    spell_id=405437,
    name="Gloom Conflagration",
    duration=5,
    color="#bf4747",
    icon="inv_shadowflame_nova.jpg",
    show=True,
)


# Tank Hit (+Frontal right after)
# 403699 + 403203
boss.add_cast(
    spell_id=405914,
    name="Withering Vulnerability",
    duration=2,
    color="#478fb3",
    icon="inv_shadowflame_buff.jpg",
    show=False,
)
