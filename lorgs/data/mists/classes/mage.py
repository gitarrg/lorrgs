"""Define the Mage Class and its Specs (MoP Classic)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.roles import RDPS
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
MAGE_ARCANE = WowSpec(id=62, index=1, role=RDPS, wow_class=MAGE, name="Arcane")
MAGE_FIRE = WowSpec(id=63, index=2, role=RDPS, wow_class=MAGE, name="Fire")
MAGE_FROST = WowSpec(id=64, index=3, role=RDPS, wow_class=MAGE, name="Frost")

################################################################################
# Spells
#
MAGE.add_spell(spell_id=80353,  cooldown=300, duration=40, name="Time Warp",                       icon="ability_mage_timewarp.jpg", tags=[SpellTag.RAID_CD])
MAGE.add_spell(spell_id=45438,  cooldown=300, duration=10, name="Ice Block",                       icon="spell_frost_frost.jpg", show=False, tags=[SpellTag.DEFENSIVE])
MAGE.add_spell(spell_id=55342,  cooldown=180, duration=30, name="Mirror Image",                    icon="spell_magic_lesserinvisibilty.jpg", show=False)
MAGE.add_spell(spell_id=108978, cooldown=180, duration=6,  name="Alter Time",                      icon="spell_mage_altertime.jpg", show=False, tags=[SpellTag.DEFENSIVE])
MAGE.add_spell(spell_id=12051,  cooldown=120, duration=6,  name="Evocation",                       icon="spell_nature_purge.jpg", show=False)

MAGE_ARCANE.add_spell(spell_id=12042,  cooldown=90,  duration=15, name="Arcane Power",                    icon="spell_nature_lightning.jpg", tags=[SpellTag.DAMAGE])
MAGE_ARCANE.add_spell(spell_id=12043,  cooldown=90,               name="Presence of Mind",                icon="spell_nature_enchantarmor.jpg", show=False)

MAGE_FROST.add_spell(spell_id=12472,  cooldown=180, duration=20, name="Icy Veins",                       icon="spell_frost_coldhearted.jpg", tags=[SpellTag.DAMAGE])
MAGE_FROST.add_spell(spell_id=11958,  cooldown=180,              name="Cold Snap",                       icon="spell_frost_wizardmark.jpg", show=False, tags=[SpellTag.DEFENSIVE])
MAGE_FROST.add_spell(spell_id=84714,  cooldown=60,               name="Frozen Orb",                      icon="spell_frost_frozenorb.jpg")
