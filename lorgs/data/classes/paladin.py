# """Define the Paladin Class and all  its Specs and Spells."""

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
PALADIN = WowClass(id=2, name="Paladin", color="#F48CBA")

################################################################################
# Specs
#
PALADIN_HOLY        = WowSpec(id=65, index=1, role=HEAL, wow_class=PALADIN, name="Holy")
PALADIN_PROTECTION  = WowSpec(id=66, index=2, role=TANK, wow_class=PALADIN, name="Protection",  short_name="Prot")
PALADIN_RETRIBUTION = WowSpec(id=70, index=3, role=MDPS, wow_class=PALADIN, name="Retribution", short_name="Ret")

################################################################################
# Spells
#

# Shared
PALADIN.add_spell(             spell_id=375576, cooldown=60,               color=COL_KYR,   name="Divine Toll",                     icon="ability_bastion_paladin.jpg",               show=False, tags=[SpellTag.DAMAGE])
PALADIN.add_spell(             spell_id=31884,  cooldown=120, duration=20, color="#ffc107", name="Avenging Wrath",                  icon="inv_ability_paladin_divinetoll.jpg", variations=[231895], tags=[SpellTag.RAID_CD])
PALADIN.add_spell(             spell_id=6940,   cooldown=120, duration=12,                  name="Blessing of Sacrifice",           icon="spell_holy_sealofsacrifice.jpg", show=False)

# Defensive
PALADIN.add_spell(             spell_id=642,    cooldown=300, duration=8,                   name="Divine Shield",                   icon="spell_holy_divineshield.jpg",     show=False, tags=[SpellTag.DEFENSIVE])
PALADIN.add_spell(             spell_id=498,    cooldown=60,  duration=8,                   name="Divine Protection",               icon="spell_holy_divineprotection.jpg", show=False, variations=[403876], tags=[SpellTag.DEFENSIVE])

# Offensive
PALADIN_HOLY.add_spell(        spell_id=31821,  cooldown=180, duration=8,  color="#dc65f5", name="Aura Mastery",                    icon="spell_holy_auramastery.jpg", tags=[SpellTag.RAID_CD])
PALADIN_HOLY.add_spell(        spell_id=200025, cooldown=15,  duration=8,  color="#e3ca09", name="Beacon of Virtue",                icon="ability_paladin_beaconofinsight.jpg", show=False)
PALADIN_HOLY.add_spell(        spell_id=216331, cooldown=60,  duration=12, color="#ffc107", name="Avenging Crusader",               icon="ability_paladin_veneration.jpg", tags=[SpellTag.RAID_CD])
PALADIN_HOLY.add_spell(        spell_id=114165, cooldown=30,               color="#51df70", name="Holy Prism",                      icon="spell_paladin_holyprism.jpg", show=False)


PALADIN_PROTECTION.add_buff(   spell_id=31850,  cooldown=120, duration=8,  color="#fcea74", name="Ardent Defender",                 icon="spell_holy_ardentdefender.jpg", tags=[SpellTag.TANK])
PALADIN_PROTECTION.add_spell(  spell_id=212641, cooldown=300, duration=8,                   name="Guardian of Ancient Kings",       icon="spell_holy_heroism.jpg", variations=[86659], tags=[SpellTag.TANK])


PALADIN_RETRIBUTION.add_spell( spell_id=255937, cooldown=45,  duration=15, color="#ff6e07", name="Wake of Ashes",      icon="inv_sword_2h_artifactashbringerfire_d_03.jpg")
PALADIN_RETRIBUTION.add_spell( spell_id=343527, cooldown=60,  duration=8,                   name="Execution Sentence", icon="spell_paladin_executionsentence.jpg")
