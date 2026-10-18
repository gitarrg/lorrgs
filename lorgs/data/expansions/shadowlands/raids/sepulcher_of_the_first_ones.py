"""RaidZone and Bosses for Patch 9.2 T29: Sepulcher of the First Ones, third tier of Shadowlands."""

# pylint: disable=line-too-long
# pylint: disable=C0326  # spaces
# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone


################################################################################################################################################################
#
#   Tier: 29 Sepulcher of the First Ones
#
################################################################################################################################################################
SEPULCHER_OF_THE_FIRST_ONES = RaidZone(id=29, name="Sepulcher of the First Ones", icon="inv_achievement_raid_progenitorraid.jpg")


################################################################################
# 01: Vigilant Guardian
VIGILANT_GUARDIAN = SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2512, name="Vigilant Guardian", icon="inv_achievement_raid_progenitorraid_progenitor_defensewall_boss.jpg")
VIGILANT_GUARDIAN.add_cast(spell_id=364962, duration=999, name="Core Overload", icon="spell_fire_selfdestruct.jpg")
VIGILANT_GUARDIAN.add_buff(spell_id=360412, duration=10,  name="Exposed Core", icon="inv_radientazeritecore.jpg")
VIGILANT_GUARDIAN.add_cast(spell_id=367561,               name="Overlock", icon="inv_misc_pocketwatch_01.jpg")
VIGILANT_GUARDIAN.add_buff(spell_id=366822,               name="Radiocative Core", icon="inv_achievement_raid_progenitorraid_progenitor_defensewall_boss.jpg")
VIGILANT_GUARDIAN.add_cast(spell_id=366692,               name="Refracted Blast", icon="6bf_explosive_shard.jpg")
VIGILANT_GUARDIAN.add_buff(spell_id=360202,               name="Spike of Creation", icon="ability_skyreach_empower.jpg")
VIGILANT_GUARDIAN.add_cast(spell_id=359608,               name="Deresolution", icon="sha_ability_mage_firestarter_nightmare.jpg")
VIGILANT_GUARDIAN.add_buff(spell_id=364881, duration=6, name="Matter Dissolution", icon="inv_progenitor_runevessel.jpg")
VIGILANT_GUARDIAN.add_buff(spell_id=364904, duration=10, name="Anti-Matter", icon="inv_progenitor_runevessel.jpg")
VIGILANT_GUARDIAN.add_cast(spell_id=360162, name="Split Resolution", icon="spell_fire_ragnaros_splittingblow.jpg")
VIGILANT_GUARDIAN.add_buff(spell_id=364843, name="Fractured Core", icon="inv_achievement_raid_progenitorraid_progenitor_defensewall_boss.jpg")
VIGILANT_GUARDIAN.add_buff(spell_id=360414, duration=45, name="Pneumatic Impact", icon="inv_blacksmithing_815_khazgorianhammer.jpg")


################################################################################
# 02: Skolex, the Insatiable Ravener
SKOLEX = SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2542, name="Skolex, the Insatiable Ravener", nick="Skolex", icon="inv_achievement_raid_progenitorraid_progenium_devourer_worm.jpg")
SKOLEX.add_cast(spell_id=359770, duration=7.0, color="#19d9e3", name="Ravening Burrow", icon="ability_argus_soulburst.jpg")  # Phase Trigger
SKOLEX.add_cast(spell_id=360451, duration=6.5, color="#9919e3", name="Retch", icon="spell_nature_acid_01.jpg")              # Frontal
SKOLEX.add_cast(spell_id=359829, duration=2.5, color="#e3ad19", name="Dust Flail", icon="ability_butcher_whirl.jpg")        # Debuff Stacks
SKOLEX.add_cast(spell_id=359975, duration=2.5, color="", name="Riftmaw", icon="inv_netherportal.jpg", show=False)
SKOLEX.add_cast(spell_id=359979, duration=2.5, color="", name="Rend", icon="inv_sword_2h_artifactsoulrend_d_06.jpg", show=False)
SKOLEX.add_cast(spell_id=364622, duration=0.0, color="", name="Final Consumption", icon="spell_shadow_unholyfrenzy.jpg")


################################################################################
# 03: Artificer Xy'mox
XYMOX = SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2553, name="Artificer Xy'mox", nick="Xy'mox", icon="inv_achievement_raid_progenitorraid_broker_incursion.jpg")
XYMOX.add_cast(spell_id=362801, duration=5.5, color="#e61919", name="Glyph of Relocation", icon="inv_axe_2h_broker_c_01.jpg")  # Tank Grip
XYMOX.add_cast(spell_id=364465,               color="", name="Forerunner Rings",    icon="spell_broker_groundstate.jpg")  # Rings
XYMOX.add_cast(spell_id=362721, duration=8.0, color="#ffc800", name="Dimensional Tear",    icon="spell_arcane_portalironforge.jpg")  # Portals
XYMOX.add_buff(spell_id=367573,               color="#00ff00", name="Genesis Bulwark",     icon="inv_progenitor_runevessel.jpg")  # Intermission
XYMOX.add_cast(spell_id=362885, duration=2.0, color="#00ffea", name="Stasis Trap",         icon="spell_broker_buff.jpg")


################################################################################
# 04: Dausegne, the Fallen Oracle
DAUSEGNE = SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2540, name="Dausegne, the Fallen Oracle", nick="Dausegne", icon="inv_achievement_raid_progenitorraid_dominated_progenitor_bot.jpg")
DAUSEGNE.add_cast(spell_id=362805, duration=10,  name="Disintegration Halo", color="#ff3333", icon="spell_progenitor_areadenial.jpg")
DAUSEGNE.add_buff(spell_id=361651,               name="Siphoned Barrier",    color="#33ff33", icon="inv_inscription_vantusrune_progenitor.jpg")
DAUSEGNE.add_cast(spell_id=360960, duration=6,   name="Staggering Barrage",  color="#aa33ff", icon="spell_progenitor_beam.jpg")
DAUSEGNE.add_cast(spell_id=361513, duration=3,   name="Obliteration Arc",    color="#4da6ff", icon="spell_progenitor_missile.jpg")
DAUSEGNE.add_cast(spell_id=359483, duration=3.4, name="Domination Core",     color="#ffdd33", icon="spell_progenitor_orb2.jpg")


################################################################################
# 05: Prototype Pantheon
PANTHEON = SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2544, name="Prototype Pantheon", icon="inv_achievement_raid_progenitorraid_proto_primus.jpg")
# Necro
PANTHEON.add_cast(spell_id=360295, duration=30, name="Necrotic Ritual", color="#33ffbb", icon="ability_warlock_cremation.jpg")  # Boss Cast
PANTHEON.add_cast(spell_id=360687, duration=2,  name="Runecarver's Deathtouch", color="#8a2ee6", icon="spell_necro_deathsdoor.jpg", show=False)
# NF
PANTHEON.add_cast(spell_id=361568, duration=3,  name="Withering Seeds",     color="#3480eb", icon="ability_ardenweald_mage.jpg")
# Venthyr
PANTHEON.add_cast(spell_id=361789, duration=6,  name="Hand of Destruction", color="#e62e2e", icon="spell_shadow_unholystrength.jpg")
PANTHEON.add_cast(spell_id=365126, duration=2,  name="Wracking Pain",       color="#e6b82e", icon="spell_animarevendreth_wave.jpg", show=False)
# Kyrian
PANTHEON.add_cast(spell_id=364941, duration=12,  name="Windswept Wings", color="#2ee6e6", icon="inv_icon_wing06b.jpg")


################################################################################
# 06: Lihuvim, Principal Architect
LIHUVIM = SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2539, name="Lihuvim, Principal Architect", nick="Lihuvim", icon="inv_achievement_raid_progenitorraid_terrestrial_keeper.jpg")
LIHUVIM.add_cast(spell_id=364652, duration=1.9, color="#e61919", name="Protoform Cascade (Frontal)",      icon="spell_progenitor_debuff.jpg")
LIHUVIM.add_cast(spell_id=362601, duration=1.9, color="#00ffea", name="Unstable Mote (Mines)",            icon="spell_progenitor_orb.jpg")
LIHUVIM.add_cast(spell_id=363088, duration=3.0, color="#ffc800", name="Cosmic Shift (Knock)",             icon="spell_progenitor_areadenial.jpg")
LIHUVIM.add_cast(spell_id=363130, duration=4,   color="#00ff00", name="Synthesize (Intermission start)",  icon="spell_progenitor_beam.jpg")
LIHUVIM.add_cast(spell_id=361200, duration=20,  color="#00ff00", name="Recharge (intermission / mythic)", icon="spell_progenitor_buff.jpg")


################################################################################
# 07: Halondrus the Reclaimer
HALONDRUS = SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2529, name="Halondrus the Reclaimer", nick="Halondrus", icon="inv_achievement_raid_progenitorraid_progenium_keeper.jpg")
HALONDRUS.add_buff(spell_id=368684,               name="Reclaim",         color="#ff3333", icon="ability_skyreach_wind.jpg")
HALONDRUS.add_buff(spell_id=359236,               name="Relocation Form", color="#3f8c49", icon="inv_progenitorbotminemount.jpg")
HALONDRUS.add_buff(spell_id=361597,               name="Ephemeral Eruption",    color="#33ffff", icon="spell_broker_nova.jpg")
HALONDRUS.add_cast(spell_id=361676, duration=1.5, name="Earthbreaker Missiles", color="#a1e617", icon="inv_misc_missilesmallcluster_yellow.jpg")
HALONDRUS.add_cast(spell_id=360977, duration=3,   name="Lightshatter Beam",     color="#fff7cc", icon="spell_progenitor_beam.jpg", show=False)
HALONDRUS.add_cast(spell_id=367079, duration=3, name="Seismic Tremors", color="#148fcc", icon="spell_sandexplosion.jpg", show=False)  # Lines + spwans Orbs
HALONDRUS.add_cast(spell_id=364979, duration=5.74, name="Shatter", color="#d517e6", icon="spell_progenitor_nova.jpg")


################################################################################
# 08: Anduin Wrynn
ANDUIN = SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2546, name="Anduin Wrynn", nick="Anduin", icon="inv_achievement_raid_progenitorraid_anduin.jpg")
ANDUIN.add_cast(spell_id=365030, duration=3.0, color="#d42020", name="Wicked Star",                       icon="spell_priest_divinestar_shadow2.jpg")
ANDUIN.add_buff(spell_id=362505,               color="#00ff00", name="Domination's Grasp (Intermission)", icon="spell_animamaw_buff.jpg")

# P1
ANDUIN.add_cast(spell_id=361989, duration=8.75, color="#a134eb", name="Blasphemy",                         icon="ability_priest_focusedwill.jpg")
ANDUIN.add_cast(spell_id=362405, duration=35,  color="#34c6eb", name="Kingsmourne Hungers",               icon="ability_deathknight_hungeringruneblade.jpg")
ANDUIN.add_cast(spell_id=365295, duration=2.0, color="#ebde34", name="Befouled Barrier",                  icon="inv_soulbarrier.jpg")

# P3
ANDUIN.add_cast(spell_id=365958, duration=2.75, color="#a134eb", name="Hopelessness",                      icon="ability_priest_halo_shadow.jpg")
ANDUIN.add_cast(spell_id=365805, duration=3.5, color="#17b6e6", name="Empowered Hopebreaker",             icon="inv_sword_1h_artifactruneblade_d_01.jpg")


################################################################################
# 09: Lords of Dread
LORDS = SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2543, name="Lords of Dread", icon="inv_achievement_raid_progenitorraid_dreadlord_duo.jpg")
LORDS.add_cast(spell_id=360300, duration=20, name="Swarm of Decay", color="#e62e2e", icon="spell_nature_naturetouchdecay.jpg")

LORDS.add_cast(spell_id=360145, duration=2 + 8, name="Fearful Trepidation", color="#5f29cc", icon="spell_nzinsanity_fearofdeath.jpg", show=False)
LORDS.add_cast(spell_id=360006, duration=2.5, name="Cloud of Carrion", color="#51cc14", icon="spell_shadow_carrionswarm.jpg", show=False)

# Among Us Intermission
LORDS.add_buff(
    spell_id=360516,
    color="#cc29b1",
    name="Among Us",
    icon="spell_nzinsanity_shortsighted.jpg",
)


################################################################################
# 10: Rygelon
RYGELON = SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2549, name="Rygelon", icon="inv_achievement_raid_progenitorraid_dominated_constellar.jpg")
RYGELON.add_buff(spell_id=363773, color="#2ee62e", name="The Singularity", icon="ability_argus_blightorb.jpg")  # Phase
RYGELON.add_cast(spell_id=362275, duration=1.0, color="#2ea9e6", name="Adds", icon="creatureportrait_sc_eyeofacherus_02.jpg")
RYGELON.add_cast(spell_id=364114, duration=5.0, color="#dd2ee6", name="Shatter Sphere", icon="spell_shadow_focusedpower.jpg")


################################################################################
# 11: The Jailer, Zovaal
JAILER = SEPULCHER_OF_THE_FIRST_ONES.add_boss(id=2537, name="The Jailer, Zovaal", nick="Jailer", icon="inv_achievement_raid_progenitorraid_jailer.jpg")
JAILER.add_cast(spell_id=360279, duration=7,   color="#FFF", name="Rune of Damnation", icon="ability_domination_rune09.jpg")
JAILER.add_cast(spell_id=363893, duration=3.6, color="#cc7b29", name="Martyrdom", icon="mace_2h_blacksmithing_d_04_icon.jpg")
JAILER.add_cast(spell_id=365212, duration=1.5, color="#FFF", name="Chains of Anguish", icon="ability_demonhunter_infernalchains.jpg")
JAILER.add_cast(spell_id=360373, duration=2,   color="#FFF", name="Unholy Attunement", icon="spell_progenitor_buff.jpg")
JAILER.add_cast(spell_id=365150, duration=6,   color="#2996cc", name="Rune of Domination", icon="ability_domination_rune10.jpg", variations=[366284])
JAILER.add_cast(spell_id=365169, duration=1.5, color="#FFF", name="Defile", icon="spell_deathknight_defile.jpg")

JAILER.add_cast(spell_id=365033, duration=6,   color="#ccc", name="Desolation", icon="spell_animamaw_missile.jpg")
JAILER.add_cast(spell_id=362028, duration=6,   color="#ccc", name="Relentless Domination", icon="inv_cape_special_domination_c_01.jpg", variations=[367851])
JAILER.add_cast(spell_id=362617, duration=6,   color="#ccc", name="Oppression", icon="spell_animamaw_wave.jpg")
JAILER.add_cast(spell_id=363332, duration=15,  color="#ccc", name="Unbreaking Grasp", icon="ability_demonhunter_illidansgrasp.jpg")
