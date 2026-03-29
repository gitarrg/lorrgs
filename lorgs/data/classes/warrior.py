"""Define the Priest Class its Specs and Spells."""

# pylint: disable=line-too-long
# pylint: disable=bad-whitespace
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.constants import *
from lorgs.data.roles import MDPS, TANK
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag, WowSpell


################################################################################
# Class
#
WARRIOR = WowClass(id=1, name="Warrior", color="#C69B6D")

################################################################################
# Specs
#
WARRIOR_ARMS          = WowSpec(id=71, index=1, role=MDPS, wow_class=WARRIOR,      name="Arms")
WARRIOR_FURY          = WowSpec(id=72, index=2, role=MDPS, wow_class=WARRIOR,      name="Fury")
WARRIOR_PROTECTION    = WowSpec(id=73, index=3, role=TANK, wow_class=WARRIOR,      name="Protection",    short_name="Prot")

################################################################################
# Spells
#
WARRIOR.add_spell(             spell_id=97462,  cooldown=180, duration=10,                  name="Rallying Cry",        icon="ability_warrior_rallyingcry.jpg",           show=False, tags=[SpellTag.RAID_CD])
WARRIOR.add_spell(             spell_id=23920,  cooldown=10,  duration=5,                   name="Spell Reflection",    icon="ability_warrior_shieldreflection.jpg",      show=False, tags=[SpellTag.DEFENSIVE])
WARRIOR.add_spell(             spell_id=107574, cooldown=90,  duration=20,                  name="Avatar",              icon="warrior_talent_icon_avatar.jpg",            show=False, variations=[401150])  # Prot uses a different Spell ID
WARRIOR.add_spell(             spell_id=446035, cooldown=90,  duration=6,                   name="Bladestorm",          icon="ability_warrior_bladestorm.jpg", tags=[SpellTag.DAMAGE])


WARRIOR_ARMS.add_spell(        spell_id=167105, cooldown=45,  duration=10, color="#ffbf29", name="Colossus Smash",      icon="ability_warrior_colossussmash.jpg",         show=False)
WARRIOR_ARMS.add_spell(        spell_id=118038, cooldown=120, duration=8,                     name="Die by the Sword",    icon="ability_warrior_challange.jpg",             show=False, tags=[SpellTag.DEFENSIVE])
WARRIOR_ARMS.add_spell(        spell_id=260708, cooldown=30,  duration=15, color="#ffbf29", name="Sweeping Strikes",    icon="ability_rogue_slicedice.jpg",       show=False)


WARRIOR_FURY.add_spell(        spell_id=1719,   cooldown=60,  duration=10,                    name="Recklessness",        icon="warrior_talent_icon_innerrage.jpg", tags=[SpellTag.DAMAGE])
WARRIOR_FURY.add_spell(        spell_id=184364, cooldown=180, duration=8,                     name="Enraged Regeneration",icon="ability_warrior_focusedrage.jpg",           show=False)
WARRIOR_FURY.add_spell(        spell_id=385059, cooldown=45,  duration=4,  color="#ffbf29", name="Odyn's Fury",         icon="inv_sword_1h_artifactvigfus_d_01.jpg",      show=False, tags=[SpellTag.DAMAGE])


WARRIOR_PROTECTION.add_spell(  spell_id=385954, cooldown=45,               color="#b34747", name="Shield Charge",       icon="ability_warrior_shieldcharge.jpg",          show=False)
WARRIOR_PROTECTION.add_spell(  spell_id=871,    cooldown=120, duration=8,  color="#039dfc", name="Shield Wall",         icon="ability_warrior_shieldwall.jpg", tags=[SpellTag.TANK])  # CD reduced by Talent per Rage spend
WARRIOR_PROTECTION.add_spell(  spell_id=1160,   cooldown=45,  duration=8,  color="#36b336", name="Demoralizing Shout",  icon="ability_warrior_warcry.jpg", show=False, tags=[SpellTag.TANK])



################################################################################
# Hero Talents
Demolish = WowSpell(
    spell_id=436358, name="Demolish",
    cooldown=45, duration=2,
    icon="inv_ability_colossuswarrior_demolish.jpg",
    show=False,
    spell_type=WARRIOR.name_slug,
)
WARRIOR_ARMS.add_spell(Demolish)
WARRIOR_PROTECTION.add_spell(Demolish)
