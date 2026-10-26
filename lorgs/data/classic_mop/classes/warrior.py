"""Define the Warrior Class and its Specs (MoP Classic)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.roles import MDPS, TANK
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag


################################################################################
# Class
#
WARRIOR = WowClass(id=1, name="Warrior", color="#C69B6D")

################################################################################
# Specs
#
WARRIOR_ARMS = WowSpec(id=71, index=1, role=MDPS, wow_class=WARRIOR, name="Arms")
WARRIOR_FURY = WowSpec(id=72, index=2, role=MDPS, wow_class=WARRIOR, name="Fury")
WARRIOR_PROTECTION = WowSpec(id=73, index=3, role=TANK, wow_class=WARRIOR, name="Protection", short_name="Prot")

################################################################################
# Spells
#
WARRIOR.add_spell(spell_id=114207, cooldown=180, duration=10, name="Skull Banner",                    icon="warrior_skullbanner.jpg", tags=[SpellTag.DAMAGE])
WARRIOR.add_spell(spell_id=114203, cooldown=180, duration=15, name="Demoralizing Banner",             icon="demoralizing_banner.jpg", show=False, tags=[SpellTag.RAID_CD])
WARRIOR.add_spell(spell_id=97462,  cooldown=180, duration=10, name="Rallying Cry",                    icon="ability_toughness.jpg", tags=[SpellTag.RAID_CD])
WARRIOR.add_spell(spell_id=107574, cooldown=180, duration=24, name="Avatar",                          icon="warrior_talent_icon_avatar.jpg", tags=[SpellTag.DAMAGE])
WARRIOR.add_spell(spell_id=114030, cooldown=120, duration=12, name="Vigilance",                       icon="ability_warrior_vigilance.jpg", show=False)

WARRIOR_ARMS.add_spell(spell_id=1719,   cooldown=180, duration=12, name="Recklessness",                    icon="ability_criticalstrike.jpg", tags=[SpellTag.DAMAGE])
WARRIOR_ARMS.add_spell(spell_id=118038, cooldown=120, duration=8,  name="Die by the Sword",                icon="ability_warrior_challange.jpg", show=False, tags=[SpellTag.DEFENSIVE])

WARRIOR_FURY.add_spell(spell_id=1719,   cooldown=180, duration=12, name="Recklessness",                    icon="ability_criticalstrike.jpg", tags=[SpellTag.DAMAGE])

WARRIOR_PROTECTION.add_spell(spell_id=871,    cooldown=180, duration=12, name="Shield Wall",                     icon="ability_warrior_shieldwall.jpg", tags=[SpellTag.TANK])
WARRIOR_PROTECTION.add_spell(spell_id=12975,  cooldown=180, duration=20, name="Last Stand",                      icon="spell_holy_ashestoashes.jpg", tags=[SpellTag.TANK])
