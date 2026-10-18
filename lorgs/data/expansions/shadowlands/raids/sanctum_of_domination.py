"""RaidZone and Bosses for Patch 9.1 T28: Sanctum of Domination, the second tier of Shadowlands."""

# pylint: disable=line-too-long
# pylint: disable=C0326  # spaces
# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone


################################################################################################################################################################
#
#   Tier: 27 Sanctum of Domination
#
################################################################################################################################################################
SANCTUM_OF_DOMINATION = RaidZone(id=28, name="Sanctum of Domination", icon="achievement_raid_torghastraid.jpg")

################################################################################
# 01: Tarragrue
TARRAGRUE = SANCTUM_OF_DOMINATION.add_boss(id=2423, name="The Tarragrue", nick="Tarragrue", icon="achievement_raid_torghast_tarragrue.jpg")
TARRAGRUE.add_buff(spell_id=347740, duration=15, color="#03d7fc", name="Hungering Mist", icon="ability_argus_soulburst.jpg")
TARRAGRUE.add_buff(spell_id=347369, duration=180, color="#ff4747", name="The Jailer's Gaze", icon="spell_animamaw_debuff.jpg")

################################################################################
# 02: Eye of the Jailer
EYE_OF_THE_JAILER = SANCTUM_OF_DOMINATION.add_boss(id=2433, name="The Eye of the Jailer", nick="The Eye", icon="achievement_raid_torghast_theeyeofthejailer.jpg")
EYE_OF_THE_JAILER.add_cast(spell_id=349030, duration=8, color="#24c9b1", name="Titanic Death Gaze",  icon="ability_argus_deathfog.jpg")
EYE_OF_THE_JAILER.add_cast(spell_id=350828, duration=2, color="#ede080", name="Deathlink",           icon="ability_felarakkoa_eyeofterrok.jpg")
EYE_OF_THE_JAILER.add_buff(spell_id=348974, color="#ff4747", name="Immediate Extermination",         icon="ability_blackhand_marked4death.jpg")
EYE_OF_THE_JAILER.add_buff(spell_id=355240, color="#db8823", name="Scorn & Ire",         icon="ability_xavius_darkruination.jpg")


################################################################################
# 03: The Nine
THE_NINE = SANCTUM_OF_DOMINATION.add_boss(id=2429, name="The Nine", icon="achievement_raid_torghast_thenine.jpg")
THE_NINE.add_cast(spell_id=350039, duration=8,  color="#47eaff", name="Arthura's Crushing Gaze", icon="spell_ice_lament.jpg")
THE_NINE.add_cast(spell_id=355294, duration=12, color="#a1b2cc", name="Resentment",              icon="spell_animamaw_buff.jpg")
THE_NINE.add_cast(spell_id=350542, duration=12, color="#2977ff", name="Fragments of Destiny",    icon="spell_frost_ice-shards.jpg")


################################################################################
# 04: Remnant of Ner'zhul
REMNANT = SANCTUM_OF_DOMINATION.add_boss(id=2432, name="Remnant of Ner'zhul", nick="Ner'zhul", icon="achievement_raid_torghast_shadowscourge_prisonofnerzhul.jpg")
REMNANT.add_cast(spell_id=350469, duration=10,  color="#9e4cc2", name="Malevolence", icon="ability_warlock_eradication.jpg")
REMNANT.add_cast(spell_id=351066, duration=2.6, color="#ff4747", name="Shatter",     icon="achievement_boss_lichking.jpg")
REMNANT.add_cast(spell_id=351073, duration=2.6, color="#ff4747", name="Shatter",     icon="inv_misc_desecrated_platechest.jpg")
REMNANT.add_cast(spell_id=351067, duration=2.6, color="#ff4747", name="Shatter",     icon="inv_misc_desecrated_plategloves.jpg")


################################################################################
# 05: Soulrender Dormazain
SOULRENDER = SANCTUM_OF_DOMINATION.add_boss(id=2434, name="Soulrender Dormazain", nick="Soulrender", icon="achievement_raid_torghast_soulrenderdormazain.jpg")
SOULRENDER.add_cast(spell_id=350615, duration=0, color="#24cbd1", name="Adds", icon="inv_mawguardpet_red.jpg")
SOULRENDER.add_cast(spell_id=352933, duration=30, color="#4cb840", name="Dance", icon="spell_animarevendreth_wave.jpg")
SOULRENDER.add_event(event_type="removedebuff", spell_id=348987, duration=9, color="#b07f6b", name="Break Shackles", icon="inv_belt_18.jpg")


################################################################################
# 06: Painsmith Raznal
PAINSMITH = SANCTUM_OF_DOMINATION.add_boss(id=2430, name="Painsmith Raznal", nick="Painsmith", icon="achievement_raid_torghast_painsmithraznal.jpg")
PAINSMITH.add_cast(spell_id=359033, duration=45, color="#30c235", name="Intermission",  icon="ability_mage_moltenarmor.jpg")
PAINSMITH.add_cast(spell_id=355571, duration=6, color="#3fd4cf", name="Axe",           icon="inv_axe_2h_mawraid_diff.jpg")
PAINSMITH.add_cast(spell_id=348513, duration=6, color="#3fd4cf", name="Hammer",        icon="inv_mace_2h_maw_c_01.jpg")
PAINSMITH.add_cast(spell_id=355787, duration=6, color="#3fd4cf", name="Scythe",        icon="inv_polearm_2h_mawnecromancerboss_d_01_grey.jpg")
# we only filter tank debuffs to minimize the number of events returned
PAINSMITH.add_event(event_type="applydebuff", spell_id=356870, duration=1.5, color="#db5f39", name="Flameclasp Trap",  icon="ability_hunter_steeltrap.jpg", extra_filter="target.role='tank'")


################################################################################
# 07: Guardian of the First Ones
GUARDIAN = SANCTUM_OF_DOMINATION.add_boss(id=2436, name="Guardian of the First Ones", nick="Guardian", icon="achievement_raid_torghast_guardianofthefirstones.jpg")
GUARDIAN.add_cast(spell_id=352538, duration=5, color="#24d1ce", name="Purging Protocol",  icon="spell_progenitor_areadenial.jpg")
GUARDIAN.add_cast(spell_id=350732, duration=2, color="#a42cd4", name="Sunder",            icon="inv_warbreaker.jpg")
GUARDIAN.add_cast(spell_id=355352, duration=2, color="#d4a72c", name="Obliterate",        icon="spell_progenitor_orb2.jpg")
GUARDIAN.add_cast(spell_id=352589, duration=6, color="#75d42c", name="Meltdown",          icon="spell_progenitor_nova.jpg")


################################################################################
# 08: Fatescribe Roh-Kalo
FATESCRIBE = SANCTUM_OF_DOMINATION.add_boss(id=2431, name="Fatescribe Roh-Kalo", nick="Fatescribe", icon="achievement_raid_torghast_guardianofthefirstones.jpg")
FATESCRIBE.add_cast(spell_id=354265, duration=6, color="#af24ff", name="Twist Fate",  icon="spell_animamaw_debuff.jpg")
FATESCRIBE.add_cast(spell_id=351680, duration=8, color="#ffda24", name="Destiny",  icon="spell_animamaw_buff.jpg")
FATESCRIBE.add_buff(spell_id=357739, color="#4bbf68", name="Intermisson", icon="spell_shadow_painfulafflictions.jpg")


################################################################################
# 09: Kel'Thuzad
KELTHUZAD = SANCTUM_OF_DOMINATION.add_boss(id=2422, name="Kel'Thuzad", icon="achievement_raid_torghast_kel-thuzad.jpg")
KELTHUZAD.add_cast(spell_id=362569, duration=8, color="#03eaff", name="Frost Blast",  icon="spell_frost_glacier.jpg", variations=[358999])  # different ID for last phase
KELTHUZAD.add_cast(spell_id=362565, duration=0, color="#03fcc6", name="Soul Fracture",  icon="spell_necro_deathlyecho.jpg", show=False)
KELTHUZAD.add_buff(spell_id=362494, color="#c7eaff", name="Howling Blizzard",  icon="spell_frost_arcticwinds.jpg")
KELTHUZAD.add_event(event_type="applydebuff", spell_id=346530, duration=10, color="#ff4538", name="Spike",  icon="ability_mage_coldasice.jpg", extra_filter="target.role='tank'")

# for the KT intermission, there is no easy way to track its duration..
# 05.01.2024: Disabled to avoid "Spell has no Icon"-Error Messages
# KELTHUZAD.add_event(
#     color="#933ac9", name="Intermisson", icon="spell_warlock_darkregeneration.jpg",
#     event_type="begincast", spell_id=352293, # start = begincast of the 45sec channel
#     until={"event_type": "applybuffstack", "spell_id": 352051} # end = gaining a stack of the Necrotic Surge
# )


################################################################################
# 10: Sylvanas Windrunner
SYLVANAS = SANCTUM_OF_DOMINATION.add_boss(id=2435, name="Sylvanas Windrunner", nick="Sylvanas", icon="achievement_raid_torghast_sylvanaswindrunner.jpg")
SYLVANAS.add_cast(spell_id=347726, duration=5, color="#228c89", name="Veil of Darkness", icon="ability_argus_deathfog.jpg", variations=[347741, 354142])

# P1
SYLVANAS.add_cast(spell_id=349419, duration=7, color="#00aaff", name="Chains", icon="inv_belt_44.jpg")
SYLVANAS.add_cast(spell_id=358704, duration=1.5, color="#ff4f42", name="Arrow", icon="ability_theblackarrow.jpg")
SYLVANAS.add_cast(spell_id=347670, duration=9, color="#7820e3", name="Shadow Dagger", icon="ability_throw.jpg")

# P2
SYLVANAS.add_cast(spell_id=351117, duration=9, color="#a76ded", name="Crushing Dread", icon="spell_shadow_gathershadows.jpg")
SYLVANAS.add_cast(spell_id=348109, duration=9, color="#3cb5ab", name="Banshee Wail", icon="spell_shadow_soulleech_3.jpg", show=False)
SYLVANAS.add_cast(spell_id=356021, duration=2, color="#eb4034", name="Dark Communion (Orbs)", icon="spell_animamaw_buff.jpg", show=True)

# P3
SYLVANAS.add_cast(spell_id=351353, duration=1, color="##ff425b", name="Banshee's Fury", icon="spell_shadow_shadowfury.jpg")
SYLVANAS.add_cast(spell_id=354011, duration=0.5, color="#9442ff", name="Bane Arrows", icon="spell_shadow_painspike.jpg")
SYLVANAS.add_cast(spell_id=347609, duration=3, color="#ff4f42", name="Wailing Arrow", icon="ability_theblackarrow.jpg")
SYLVANAS.add_cast(spell_id=354068, duration=1, color="#921de0", name="Banshee's Fury", icon="spell_shadow_shadowfury.jpg")
