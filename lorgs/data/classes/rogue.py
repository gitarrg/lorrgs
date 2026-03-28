"""Define the Rogue Class and all its Specs and Spells."""

# pylint: disable=line-too-long
# pylint: disable=bad-whitespace
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.constants import *
from lorgs.data.roles import *
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag


################################################################################
# Class
#
ROGUE = WowClass(id=4, name="Rogue", color="#FFF468")

################################################################################
# Specs
#
ROGUE_ASSASSINATION = WowSpec(id=259, role=MDPS, wow_class=ROGUE, name="Assassination", short_name="Assa")
ROGUE_OUTLAW        = WowSpec(id=260, role=MDPS, wow_class=ROGUE, name="Outlaw")
ROGUE_SUBTLETY      = WowSpec(id=261, role=MDPS, wow_class=ROGUE, name="Subtlety")

################################################################################
# Spells
#
ROGUE.add_spell(spell_id=1856,   cooldown=120,              color="#999999", name="Vanish",              icon="ability_vanish.jpg",                       show=False)
ROGUE.add_spell(spell_id=385616, cooldown=45, duration=45,  color=COL_KYR,   name="Echoing Reprimand",   icon="ability_bastion_rogue.jpg",                show=False)
ROGUE.add_spell(spell_id=185313, cooldown=0,   duration=8,  color="#cf5dab", name="Shadow Dance",        icon="ability_rogue_shadowdance.jpg",            show=False)

ROGUE.add_spell(               spell_id=31224,  cooldown=60,  duration=5,                   name="Cloak of Shadows",    icon="spell_shadow_nethercloak.jpg",             show=False, tags=[SpellTag.DEFENSIVE])
ROGUE.add_buff(                spell_id=45182,  cooldown=360, duration=3,                   name="Cheating Death",      icon="ability_rogue_cheatdeath.jpg",             show=False, tags=[SpellTag.DEFENSIVE])
ROGUE.add_spell(               spell_id=5277,   cooldown=120, duration=10,                  name="Evasion",             icon="spell_shadow_shadowward.jpg",              show=False, tags=[SpellTag.DEFENSIVE])
ROGUE.add_spell(               spell_id=185311, cooldown=30,  duration=4,                   name="Crimson Vial",        icon="ability_rogue_crimsonvial.jpg",            show=False, tags=[SpellTag.DEFENSIVE])
ROGUE.add_spell(               spell_id=1966,   cooldown=15,  duration=6,                   name="Feint",               icon="ability_rogue_feint.jpg",                  show=False, tags=[SpellTag.DEFENSIVE])
ROGUE.add_spell(               spell_id=385408, cooldown=90,  duration=10, color=COL_NF,    name="Sepsis",              icon="ability_ardenweald_rogue.jpg",             show=False)

ROGUE_ASSASSINATION.add_spell( spell_id=5938,   cooldown=25,                                name="Shiv",                icon="inv_throwingknife_04.jpg",                 show=False)
ROGUE_ASSASSINATION.add_spell( spell_id=360194, cooldown=120, duration=16, color="#cc5466", name="Deathmark",           icon="ability_rogue_deathmark.jpg", tags=[SpellTag.DAMAGE])
ROGUE_ASSASSINATION.add_spell( spell_id=385627, cooldown=60,  duration=14, color="#4cc2d4", name="Kingsbane",           icon="inv_knife_1h_artifactgarona_d_01.jpg", tags=[SpellTag.DAMAGE])
ROGUE_ASSASSINATION.add_spell( spell_id=200806, cooldown=128, duration=14, color="#bf291f", name="Exsanguinate",        icon="ability_deathwing_bloodcorruption_earth.jpg")

ROGUE_SUBTLETY.add_spell(      spell_id=121471, cooldown=180, duration=20, color="#9a1be3", name="Shadow Blades",       icon="inv_knife_1h_grimbatolraid_d_03.jpg", tags=[SpellTag.DAMAGE])
ROGUE_SUBTLETY.add_spell(      spell_id=280719, cooldown=60,               color="#3638d6", name="Secret Technique",    icon="ability_rogue_sinistercalling.jpg",        show=False)
ROGUE_SUBTLETY.add_spell(      spell_id=384631, cooldown=90, duration=12,  color=COL_VENTR, name="Flagellation",        icon="ability_revendreth_rogue.jpg")
ROGUE_SUBTLETY.add_spell(      spell_id=212283, cooldown=25,  duration=10,                  name="Symbols of Death",    icon="spell_shadow_rune.jpg",                    show=False)
ROGUE_SUBTLETY.add_spell(      spell_id=277925, cooldown=60,  duration=5,  color="#ffee00", name="Shuriken Tornado",    icon="ability_rogue_throwingspecialization.jpg")
ROGUE_SUBTLETY.add_spell(      spell_id=382245, cooldown=45,               color="#4cc2d4", name="Cold Blood",    icon="spell_ice_lament.jpg", show=False)


ROGUE_OUTLAW.add_spell(        spell_id=13750,  cooldown=0,   duration=20,                  name="Adrenaline Rush",     icon="spell_shadow_shadowworddominate.jpg", tags=[SpellTag.DAMAGE])
ROGUE_OUTLAW.add_spell(        spell_id=315508,               duration=30, color="#c7813c", name="Roll the Bones",      icon="ability_rogue_rollthebones.jpg",           show=False)
ROGUE_OUTLAW.add_spell(        spell_id=51690,  cooldown=120,                               name="Killing Spree",       icon="ability_rogue_murderspree.jpg", tags=[SpellTag.DAMAGE])
ROGUE_OUTLAW.add_spell(        spell_id=343142, cooldown=120, duration=8,  color="#3d9991", name="Dreadblades",         icon="inv_sword_1h_artifactskywall_d_01dual.jpg", show=False, tags=[SpellTag.DAMAGE])
ROGUE_OUTLAW.add_spell(        spell_id=381989, cooldown=0,   duration=30, color="#b3702d", name="Keep It Rolling",     icon="ability_rogue_keepitrolling.jpg")
