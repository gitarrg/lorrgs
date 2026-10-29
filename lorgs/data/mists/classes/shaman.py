"""Define the Shaman Class and its Specs (MoP Classic)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.mists.roles import HEAL, MDPS, RDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag


################################################################################
# Class
#
SHAMAN = WowClass(id=7, name="Shaman", color="#0070DD")

################################################################################
# Specs
#
SHAMAN_ELEMENTAL = WowSpec(id=262, index=1, role=RDPS, wow_class=SHAMAN, name="Elemental")
SHAMAN_ENHANCEMENT = WowSpec(id=263, index=2, role=MDPS, wow_class=SHAMAN, name="Enhancement")
SHAMAN_RESTORATION = WowSpec(id=264, index=3, role=HEAL, wow_class=SHAMAN, name="Restoration", short_name="Resto")

################################################################################
# Spells
#
SHAMAN.add_spell(spell_id=2825,   cooldown=300, duration=40, name="Bloodlust",                       icon="spell_nature_bloodlust.jpg", variations=[32182], tags=[SpellTag.RAID_CD])
SHAMAN.add_spell(spell_id=120668, cooldown=300, duration=10, name="Stormlash Totem",                 icon="ability_shaman_tranquilmindtotem.jpg", tags=[SpellTag.DAMAGE])
SHAMAN.add_spell(spell_id=2894,   cooldown=300, duration=60, name="Fire Elemental Totem",            icon="spell_fire_elemental_totem.jpg", tags=[SpellTag.DAMAGE])
SHAMAN.add_spell(spell_id=79206,  cooldown=120, duration=15, name="Spiritwalker's Grace",            icon="spell_shaman_spiritwalkersgrace.jpg", show=False, tags=[SpellTag.MOVE])
SHAMAN.add_spell(spell_id=2062,   cooldown=300, duration=60, name="Earth Elemental Totem",           icon="spell_nature_earthelemental_totem.jpg", show=False, tags=[SpellTag.DEFENSIVE])
SHAMAN.add_spell(spell_id=108281, cooldown=120, duration=10, name="Ancestral Guidance",              icon="ability_shaman_ancestralguidance.jpg", show=False)

SHAMAN_ELEMENTAL.add_spell(spell_id=114050, cooldown=180, duration=15, name="Ascendance",                      icon="classic_spell_fire_elementaldevastation.jpg", tags=[SpellTag.DAMAGE])

SHAMAN_ENHANCEMENT.add_spell(spell_id=51533,  cooldown=120, duration=30, name="Feral Spirit",                    icon="spell_shaman_feralspirit.jpg", tags=[SpellTag.DAMAGE])
SHAMAN_ENHANCEMENT.add_spell(spell_id=114051, cooldown=180, duration=15, name="Ascendance",                      icon="classic_spell_fire_elementaldevastation.jpg", tags=[SpellTag.DAMAGE])

SHAMAN_RESTORATION.add_spell(spell_id=108280, cooldown=180, duration=10, name="Healing Tide Totem",              icon="ability_shaman_healingtide.jpg", tags=[SpellTag.RAID_CD])
SHAMAN_RESTORATION.add_spell(spell_id=98008,  cooldown=180, duration=6,  name="Spirit Link Totem",               icon="spell_shaman_spiritlink.jpg", tags=[SpellTag.RAID_CD])
SHAMAN_RESTORATION.add_spell(spell_id=16190,  cooldown=180, duration=16, name="Mana Tide Totem",                 icon="spell_frost_summonwaterelemental.jpg", tags=[SpellTag.RAID_CD])
SHAMAN_RESTORATION.add_spell(spell_id=114052, cooldown=180, duration=15, name="Ascendance",                      icon="classic_spell_fire_elementaldevastation.jpg", tags=[SpellTag.RAID_CD])
