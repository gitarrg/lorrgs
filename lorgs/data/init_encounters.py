#!/usr/bin/env python
"""Models for Raids and RaidBosses."""

# pylint: disable=line-too-long
# pylint: disable=C0326  # spaces

# IMPORT LOCAL LIBRARIES
from lorgs.models.encounters import RaidZone

################################################################################################################################################################
#
#   Tier: 26 Castle Nathria
#
################################################################################################################################################################
CASTLE_NATHRIA = RaidZone(id=26, name="Castle Nathria")

################################################################################
# 01: Shriekwing
SHRIEKWING = CASTLE_NATHRIA.add_boss(id=2398, name="Shriekwing")
SHRIEKWING.add_event(event_type="cast",      spell_id=345397, duration=12, color="#c94444", name="Wave of Blood",   icon="ability_ironmaidens_whirlofblood.jpg")
SHRIEKWING.add_event(event_type="cast",      spell_id=342863,              color="#c94444", name="Echoing Screech", icon="spell_nature_wispsplode.jpg")
SHRIEKWING.add_event(event_type="applybuff", spell_id=328921, duration=33, color="#999999", name="Blood Shroud",    icon="ability_deathwing_bloodcorruption_earth.jpg")

CASTLE_NATHRIA.add_boss(id=2418, name="Huntsman Altimor")

################################################################################
# 03: Hungering Destroyer
HUNGERING_DESTROYER = CASTLE_NATHRIA.add_boss(id=2383, name="Hungering Destroyer")
HUNGERING_DESTROYER.add_event(event_type="begincast", spell_id=334522, duration=10, color="#17e3be", name="Consume",  icon="ability_argus_deathfog.jpg")
HUNGERING_DESTROYER.add_event(event_type="cast",      spell_id=329455, duration=10, color="#d65656", name="Desolate", icon="ability_argus_soulburst.jpg")

CASTLE_NATHRIA.add_boss(id=2402, name="Sun King's Salvation")

CASTLE_NATHRIA.add_boss(id=2405, name="Artificer Xy'mox")

CASTLE_NATHRIA.add_boss(id=2406, name="Lady Inerva Darkvein")

CASTLE_NATHRIA.add_boss(id=2412, name="The Council of Blood")

################################################################################
# 08: Sludgefist
SLUDGEFIST = CASTLE_NATHRIA.add_boss(id=2399, name="Sludgefist")
SLUDGEFIST.add_event(event_type="cast",      spell_id=332687, name="Colossal Roar",      icon="ability_garrosh_hellscreams_warsong.jpg", duration=2, color="#c94444")
SLUDGEFIST.add_event(event_type="cast",      spell_id=332318, name="Destructive Stomp",  icon="spell_nature_earthquake.jpg", duration=4, color="#d69429")
SLUDGEFIST.add_event(event_type="applybuff", spell_id=331314, name="Destructive Impact", icon="spell_frost_stun.jpg", duration=12, color="#34c0eb")

################################################################################
# 09: Stone Legion Generals
SLG = CASTLE_NATHRIA.add_boss(id=2417, name="Stone Legion Generals")
SLG.add_event(event_type="cast",      spell_id=342544, name="Pulverizing Meteor",  icon="inv_elementalearth2.jpg", duration=2, color="#d69429")
SLG.add_event(event_type="cast",      spell_id=334498, name="Seismic Upheaval",  icon="spell_nature_earthquake.jpg", duration=5, color="#d69429")
SLG.add_event(event_type="cast",      spell_id=334765, name="Heart Rend",  icon="spell_fire_flameblades.jpg", duration=36, color="#d69429", show=False)

################################################################################
# 10: Sire Denathrius
SIRE_DENATHRIUS = CASTLE_NATHRIA.add_boss(id=2407, name="Sire Denathrius")
SIRE_DENATHRIUS.add_event(event_type="cast", spell_id=326994, duration=3.5, color="#c94444", name="Blood Price",           icon="ability_ironmaidens_whirlofblood.jpg")
SIRE_DENATHRIUS.add_event(event_type="cast", spell_id=326707, duration=3,   color="#0083ff", name="Cleansing Pain",        icon="spell_animarevendreth_wave.jpg")
SIRE_DENATHRIUS.add_event(event_type="cast", spell_id=327122, duration=6,   color="#ffcf00", name="Ravage",                icon="spell_shadow_corpseexplode.jpg", show=False)

SIRE_DENATHRIUS.add_event(event_type="cast", spell_id=328117, duration=10,  color="#ffffff", name="March of the Penitent", icon="sha_spell_shadow_shadesofdarkness_nightmare.jpg")

# P2
SIRE_DENATHRIUS.add_event(event_type="cast", spell_id=333932, duration=0, color="#c94444", name="Hand of Destruction",     icon="spell_shadow_unholystrength.jpg")
SIRE_DENATHRIUS.add_event(event_type="cast", spell_id=329943, duration=0, color="#c94444", name="Impale",                  icon="ability_backstab.jpg")

# P3
SIRE_DENATHRIUS.add_event(event_type="cast", spell_id=332937, duration=6,   color="#ffcf00", name="Ravage",                icon="spell_shadow_corpseexplode.jpg", show=False)
SIRE_DENATHRIUS.add_event(event_type="cast", spell_id=332619, duration=3,   color="#0083ff", name="Shattering Pain",       icon="sha_spell_fire_blueflamestrike_nightmare.jpg")

CASTLE_NATHRIA_BOSSES = CASTLE_NATHRIA.bosses

DEFAULT_BOSS = SIRE_DENATHRIUS
