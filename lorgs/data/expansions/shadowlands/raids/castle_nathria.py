"""RaidZone and Bosses for the T26: Castle Nathria, the first Tier of Shadowlands."""

# pylint: disable=line-too-long
# pylint: disable=C0326  # spaces
# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone


GREEN = "#2ee62e"  # HSV: 120, 80, 90


################################################################################################################################################################
#
#   Tier: 26 Castle Nathria
#
################################################################################################################################################################
CASTLE_NATHRIA = RaidZone(id=26, name="Castle Nathria", icon="achievement_raid_revendrethraid_castlenathria.jpg")


################################################################################
# 01: Shriekwing
SHRIEKWING = CASTLE_NATHRIA.add_boss(id=2398, name="Shriekwing", icon="achievement_raid_revendrethraid_shriekwing.jpg")
SHRIEKWING.add_cast(spell_id=345397, duration=12, color="#c94444", name="Wave of Blood",   icon="ability_ironmaidens_whirlofblood.jpg")
SHRIEKWING.add_cast(spell_id=342863, duration=3,  color="#7af6ff", name="Echoing Screech", icon="spell_nature_wispsplode.jpg")
SHRIEKWING.add_buff(spell_id=328921,              color="#3f8c49", name="Blood Shroud",    icon="ability_deathwing_bloodcorruption_earth.jpg")


################################################################################
# 02: Huntsman
HUNTSMAN = CASTLE_NATHRIA.add_boss(id=2418, name="Huntsman Altimor", icon="achievement_raid_revendrethraid_altimor.jpg")
HUNTSMAN.add_cast(spell_id=334797, duration=2.5, color="#a27aff", name="Rip Soul",        icon="ability_druid_markofursol.jpg")
HUNTSMAN.add_cast(spell_id=334942, duration=2.5, color="#cc3737", name="Vicious Lunge",   icon="ability_blackhand_marked4death.jpg")


################################################################################
# 03: Hungering Destroyer
HUNGERING_DESTROYER = CASTLE_NATHRIA.add_boss(id=2383, name="Hungering Destroyer", icon="achievement_raid_revendrethraid_hungeringdestroyer.jpg")
HUNGERING_DESTROYER.add_cast(spell_id=329455, duration=10, color="#40bfff", name="Desolate", icon="ability_argus_soulburst.jpg")
HUNGERING_DESTROYER.add_cast(spell_id=334522, duration=10, color="#3dcc85", name="Consume",  icon="ability_argus_deathfog.jpg")


################################################################################
# 04: Sun King
SUNKING = CASTLE_NATHRIA.add_boss(id=2402, name="Sun King's Salvation", nick="Sun King", icon="achievement_raid_revendrethraid_kaelthassunstrider.jpg")
SUNKING.add_cast(spell_id=343026, duration=3, color="#325873", name="Ember Blast",  icon="spell_fire_selfdestruct.jpg")
SUNKING.add_buff(spell_id=343026,             color="#ffbb33", name="Cloak of Flames (DPS)",  icon="ability_creature_cursed_01.jpg")
SUNKING.add_buff(spell_id=337859,             color="#ffbb33", name="Cloak of Flames (Heal)",  icon="ability_creature_cursed_01.jpg")
# TODO: add Phase Indicators


################################################################################
# 04: Xymox v1
XYMOX = CASTLE_NATHRIA.add_boss(id=2405, name="Artificer Xy'mox (CN)", nick="Xy'mox", icon="achievement_raid_revendrethraid_artificerxymox.jpg")
XYMOX.add_cast(spell_id=329770, duration=21.5, color="#40bfff", name="Root of Extinction (Seeds)",  icon="inv_wand_1h_ardenweald_d_01.jpg")
XYMOX.add_cast(spell_id=325361, duration=6.5,  color="#e61919", name="Glyph of Destruction",       icon="ability_mage_incantersabsorbtion.jpg")


################################################################################
# 05: Lady Inerva Darkvein
INERVA = CASTLE_NATHRIA.add_boss(id=2406, name="Lady Inerva Darkvein", nick="Inerva", icon="achievement_raid_revendrethraid_ladyinervadarkvein.jpg")
INERVA.add_cast(spell_id=342281, duration=1.5, color="#FFF", name="Lingering Anima (Soak)",  icon="ui_venthyranimaboss_bottle.jpg")
# TODO: add spell variations


################################################################################
# 06: The Council of Blood
COUNCIL_OF_BLOOD = CASTLE_NATHRIA.add_boss(id=2412, name="The Council of Blood", nick="Council", icon="achievement_raid_revendrethraid_nobilitycouncil.jpg")
COUNCIL_OF_BLOOD.add_cast(spell_id=330959, duration=36, color=GREEN,   name="Danse Macabre", icon="ability_rogue_shadowdance.jpg")
COUNCIL_OF_BLOOD.add_cast(spell_id=331634, duration=6,  color="#6735d4", name="Dark Recital", icon="ability_warlock_soullink.jpg")
COUNCIL_OF_BLOOD.add_buff(spell_id=347350, duration=30, color="#d65656", name="Dancing Fever", icon="ability_deathknight_hemorrhagicfever.jpg")


################################################################################
# 08: Sludgefist
SLUDGEFIST = CASTLE_NATHRIA.add_boss(id=2399, name="Sludgefist", icon="achievement_raid_revendrethraid_sludgefist.jpg")
SLUDGEFIST.add_cast(spell_id=332687, duration=2,  color="#c94444", name="Colossal Roar",      icon="ability_garrosh_hellscreams_warsong.jpg")
SLUDGEFIST.add_cast(spell_id=332318, duration=4,  color="#d69429", name="Destructive Stomp",  icon="spell_nature_earthquake.jpg")
SLUDGEFIST.add_buff(spell_id=331314, duration=12, color="#34c0eb", name="Destructive Impact", icon="spell_frost_stun.jpg")


################################################################################
# 09: Stone Legion Generals
SLG = CASTLE_NATHRIA.add_boss(id=2417, name="Stone Legion Generals", icon="achievement_raid_revendrethraid_generalkaalgrashaal.jpg")
SLG.add_cast(spell_id=342544, duration=2,  color="#d69429", name="Pulverizing Meteor",  icon="inv_elementalearth2.jpg")
SLG.add_cast(spell_id=334498, duration=5,  color="#d69429", name="Seismic Upheaval",    icon="spell_nature_earthquake.jpg")
SLG.add_cast(spell_id=334765, duration=36, color="#d69429", name="Heart Rend",          icon="spell_fire_flameblades.jpg", show=False)


################################################################################
# 10: Sire Denathrius
SIRE_DENATHRIUS = CASTLE_NATHRIA.add_boss(id=2407, name="Sire Denathrius", icon="achievement_raid_revendrethraid_siredenathrius.jpg")
SIRE_DENATHRIUS.add_cast(spell_id=326994, duration=3.5, color="#c94444", name="Blood Price",           icon="ability_ironmaidens_whirlofblood.jpg")
SIRE_DENATHRIUS.add_cast(spell_id=326707, duration=3,   color="#0083ff", name="Cleansing Pain",        icon="spell_animarevendreth_wave.jpg")
SIRE_DENATHRIUS.add_cast(spell_id=327122, duration=6,   color="#ffcf00", name="Ravage",                icon="spell_shadow_corpseexplode.jpg", show=False)
SIRE_DENATHRIUS.add_cast(spell_id=328117, duration=10,  color="#ffffff", name="March of the Penitent", icon="sha_spell_shadow_shadesofdarkness_nightmare.jpg")

# P2
SIRE_DENATHRIUS.add_cast(spell_id=333932, duration=0, color="#c94444", name="Hand of Destruction",     icon="spell_shadow_unholystrength.jpg")
SIRE_DENATHRIUS.add_cast(spell_id=329943, duration=0, color="#c94444", name="Impale",                  icon="ability_backstab.jpg")

# P3
SIRE_DENATHRIUS.add_cast(spell_id=332937, duration=6,   color="#ffcf00", name="Ravage",                icon="spell_shadow_corpseexplode.jpg", show=False)
SIRE_DENATHRIUS.add_cast(spell_id=332619, duration=3,   color="#0083ff", name="Shattering Pain",       icon="sha_spell_fire_blueflamestrike_nightmare.jpg")
