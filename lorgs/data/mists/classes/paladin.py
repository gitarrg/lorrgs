"""Define the Paladin Class and its Specs (MoP Classic)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.mists.roles import HEAL, MDPS, TANK
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
PALADIN_HOLY = WowSpec(id=65, index=1, role=HEAL, wow_class=PALADIN, name="Holy")
PALADIN_PROTECTION = WowSpec(id=66, index=2, role=TANK, wow_class=PALADIN, name="Protection", short_name="Prot")
PALADIN_RETRIBUTION = WowSpec(id=70, index=3, role=MDPS, wow_class=PALADIN, name="Retribution", short_name="Ret")

################################################################################
# Spells
#
PALADIN.add_spell(spell_id=31884,  cooldown=180, duration=20, name="Avenging Wrath",                  icon="spell_holy_avenginewrath.jpg", tags=[SpellTag.DAMAGE])
PALADIN.add_spell(spell_id=642,    cooldown=300, duration=8,  name="Divine Shield",                   icon="spell_holy_divineshield.jpg", show=False, tags=[SpellTag.DEFENSIVE])
PALADIN.add_spell(spell_id=633,    cooldown=600,              name="Lay on Hands",                    icon="spell_holy_layonhands.jpg", show=False)
PALADIN.add_spell(spell_id=1022,   cooldown=300, duration=10, name="Hand of Protection",              icon="spell_holy_sealofprotection.jpg", show=False)
PALADIN.add_spell(spell_id=6940,   cooldown=120, duration=12, name="Hand of Sacrifice",               icon="spell_holy_sealofsacrifice.jpg", show=False)
PALADIN.add_spell(spell_id=105809, cooldown=120, duration=18, name="Holy Avenger",                    icon="ability_paladin_holyavenger.jpg", tags=[SpellTag.DAMAGE])

PALADIN_HOLY.add_spell(spell_id=31842,  cooldown=180, duration=20, name="Divine Favor",                    icon="spell_holy_divineillumination.jpg", tags=[SpellTag.DAMAGE])
PALADIN_HOLY.add_spell(spell_id=86669,  cooldown=180, duration=15, name="Guardian of Ancient Kings",       icon="spell_holy_heroism.jpg", tags=[SpellTag.RAID_CD])
PALADIN_HOLY.add_spell(spell_id=31821,  cooldown=180, duration=6,  name="Devotion Aura",                   icon="spell_holy_auramastery.jpg", tags=[SpellTag.RAID_CD])

PALADIN_PROTECTION.add_spell(spell_id=86659,  cooldown=180, duration=12, name="Guardian of Ancient Kings",       icon="spell_holy_heroism.jpg", tags=[SpellTag.TANK])
PALADIN_PROTECTION.add_spell(spell_id=31850,  cooldown=180, duration=10, name="Ardent Defender",                 icon="spell_holy_ardentdefender.jpg", tags=[SpellTag.TANK])

PALADIN_RETRIBUTION.add_spell(spell_id=86698,  cooldown=180, duration=30, name="Guardian of Ancient Kings",       icon="spell_holy_heroism.jpg", tags=[SpellTag.DAMAGE])
