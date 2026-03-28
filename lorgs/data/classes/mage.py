"""Define the Mage Class and all its Specs and Spells."""

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
MAGE = WowClass(id=8, name="Mage", color="#3FC7EB")

################################################################################
# Specs
#
MAGE_ARCANE = WowSpec(id=62, role=RDPS, wow_class=MAGE, name="Arcane")
MAGE_FIRE   = WowSpec(id=63, role=RDPS, wow_class=MAGE, name="Fire")
MAGE_FROST  = WowSpec(id=64, role=RDPS, wow_class=MAGE, name="Frost")

################################################################################
# Spells
#
# tracked as buff (channel shows up as 4 individual casts)
MAGE.add_buff(        spell_id=382440, cooldown=60,  duration=4,  color=COL_NF,    name="Shifting Power",     icon="ability_ardenweald_mage.jpg",               show=False)

# Defensives
MAGE.add_buff(         spell_id=45438,  cooldown=240,                               name="Ice Block",          icon="spell_frost_frost.jpg",                     show=False, tags=[SpellTag.DEFENSIVE])
MAGE.add_buff(         spell_id=55342,  cooldown=120, duration=40,                  name="Mirror Image",       icon="spell_magic_lesserinvisibilty.jpg",         show=False, tags=[SpellTag.DEFENSIVE])
MAGE.add_buff(         spell_id=342246, cooldown=60,                                name="Alter Time",         icon="spell_mage_altertime.jpg",                  show=False, tags=[SpellTag.DEFENSIVE], variations=[342246])
MAGE.add_spell(        spell_id=414660, cooldown=180,                               name="Mass Barrier",       icon="ability_racial_magicalresistance.jpg",      show=False, tags=[SpellTag.DEFENSIVE])
MAGE.add_spell(        spell_id=414658, cooldown=240, duration=6,                   name="Ice Cold",           icon="spell_fire_bluefire.jpg",                   show=False, tags=[SpellTag.DEFENSIVE])
MAGE.add_buff(         spell_id=113862, cooldown=120,                               name="Greater Invisibility",icon="ability_mage_greaterinvisibility.jpg",     show=False, tags=[SpellTag.DEFENSIVE])


MAGE_ARCANE.add_buff(  spell_id=235450, cooldown=25,                                name="Prismatic Barrier",  icon="spell_magearmor.jpg",                       show=False, tags=[SpellTag.DEFENSIVE])
MAGE_FIRE.add_buff(    spell_id=235313, cooldown=25,                                name="Blazing Barrier",    icon="ability_mage_moltenarmor.jpg",              show=False, tags=[SpellTag.DEFENSIVE])
MAGE_FIRE.add_debuff(  spell_id=87023,  cooldown=300, duration=6,                   name="Cauterize",          icon="spell_fire_rune.jpg",                       show=False, tags=[SpellTag.DEFENSIVE])
MAGE_FROST.add_buff(   spell_id=11426,  cooldown=25,                                name="Ice Barrier",        icon="spell_ice_lament.jpg",                      show=False, tags=[SpellTag.DEFENSIVE])

# Offensive
MAGE.add_spell(        spell_id=116011, cooldown=45,  duration=12,                  name="Rune of Power",      icon="spell_mage_runeofpower.jpg",                show=False)
MAGE.add_buff(         spell_id=386540, duration=40,               color="#ffcc66", name="Temporal Warp",      icon="ability_bossmagistrix_timewarp2.jpg")

MAGE_FIRE.add_spell(   spell_id=190319, cooldown=60,  duration=10, color="#e3b02d", name="Combustion",         icon="spell_fire_sealoffire.jpg",      tags=[SpellTag.DYNAMIC_CD, SpellTag.DAMAGE])
MAGE_FIRE.add_spell(   spell_id=153561, cooldown=45,                                name="Meteor",             icon="spell_mage_meteor.jpg",                     show=False)
MAGE_FIRE.add_buff(    spell_id=383883,                                             name="Sun King's Blessing",icon="ability_mage_firestarter.jpg",              show=True)

MAGE_ARCANE.add_spell( spell_id=321507, cooldown=45,  duration=8,                   name="Touch of the Magi",  icon="ability_mage_netherwindpresence.jpg", tags=[SpellTag.DAMAGE])
MAGE_ARCANE.add_spell( spell_id=365350, cooldown=90,  duration=12,                  name="Arcane Surge",       icon="ability_mage_arcanesurge.jpg")
MAGE_ARCANE.add_spell( spell_id=12051,  cooldown=90,  duration=6,                   name="Evocation",          icon="spell_nature_purge.jpg", tags=[SpellTag.DAMAGE])
MAGE_ARCANE.add_spell( spell_id=376103, cooldown=30,  duration=10, color=COL_KYR,   name="Radiant Spark",      icon="ability_bastion_mage.jpg",                  show=False)
MAGE_ARCANE.add_spell( spell_id=5405,   cooldown=90,               color=COL_MANA,  name="Replenish Mana",      icon="inv_misc_gem_sapphire_02.jpg",             show=False)

MAGE_FROST.add_spell(  spell_id=12472,  cooldown=60,  duration=20,                  name="Icy Veins",          icon="spell_frost_coldhearted.jpg", tags=[SpellTag.DAMAGE])
MAGE_FROST.add_spell(  spell_id=84714,  cooldown=60,                                name="Frozen Orb",         icon="spell_frost_frozenorb.jpg")
MAGE_FROST.add_spell(  spell_id=205021, cooldown=60, duration=5,                    name="Ray of Frost",       icon="ability_mage_rayoffrost.jpg")
MAGE_FROST.add_spell(  spell_id=120,    cooldown=45,             color="#8dd1d9", name="Cone of Cold",       icon="spell_frost_glacier.jpg", show=False)
MAGE_FROST.add_spell(  spell_id=153595, cooldown=30,             color="#486ce0", name="Comet Storm",        icon="spell_mage_cometstorm2.jpg", show=False)
