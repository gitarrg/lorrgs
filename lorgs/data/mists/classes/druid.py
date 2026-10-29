"""Define the Druid Class and its Specs (MoP Classic)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.mists.roles import HEAL, MDPS, RDPS, TANK
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag


################################################################################
# Class
#
DRUID = WowClass(id=11, name="Druid", color="#FF7C0A")

################################################################################
# Specs
#
DRUID_BALANCE = WowSpec(id=102, index=1, role=RDPS, wow_class=DRUID, name="Balance")
DRUID_FERAL = WowSpec(id=103, index=2, role=MDPS, wow_class=DRUID, name="Feral")
DRUID_GUARDIAN = WowSpec(id=104, index=3, role=TANK, wow_class=DRUID, name="Guardian")
DRUID_RESTORATION = WowSpec(id=105, index=4, role=HEAL, wow_class=DRUID, name="Restoration", short_name="Resto")

################################################################################
# Spells
#
DRUID.add_spell(spell_id=77764,  cooldown=120, duration=8,  name="Stampeding Roar",                 icon="spell_druid_stampedingroar_cat.jpg", show=False, tags=[SpellTag.MOVE])
DRUID.add_spell(spell_id=29166,  cooldown=180, duration=10, name="Innervate",                       icon="spell_nature_lightning.jpg", show=False)
DRUID.add_spell(spell_id=20484,  cooldown=600,              name="Rebirth",                         icon="spell_nature_reincarnation.jpg", show=False)
DRUID.add_spell(spell_id=108288, cooldown=360, duration=45, name="Heart of the Wild",               icon="spell_holy_blessingofagility.jpg", show=False)
DRUID.add_spell(spell_id=124974, cooldown=90,  duration=30, name="Nature's Vigil",                  icon="achievement_zone_feralas.jpg", tags=[SpellTag.DAMAGE])

DRUID_BALANCE.add_spell(spell_id=112071, cooldown=180, duration=15, name="Celestial Alignment",             icon="spell_nature_natureguardian.jpg", tags=[SpellTag.DAMAGE])

DRUID_FERAL.add_spell(spell_id=106951, cooldown=180, duration=15, name="Berserk",                         icon="ability_druid_berserk.jpg", tags=[SpellTag.DAMAGE])
DRUID_FERAL.add_spell(spell_id=61336,  cooldown=180, duration=12, name="Survival Instincts",              icon="ability_druid_tigersroar.jpg", show=False, tags=[SpellTag.DEFENSIVE])

DRUID_GUARDIAN.add_spell(spell_id=50334,  cooldown=180, duration=10, name="Berserk",                         icon="ability_druid_berserk.jpg", tags=[SpellTag.TANK])
DRUID_GUARDIAN.add_spell(spell_id=106922, cooldown=180, duration=20, name="Might of Ursoc",                  icon="spell_druid_mightofursoc.jpg", tags=[SpellTag.TANK])
DRUID_GUARDIAN.add_spell(spell_id=61336,  cooldown=180, duration=12, name="Survival Instincts",              icon="ability_druid_tigersroar.jpg", tags=[SpellTag.TANK])

DRUID_RESTORATION.add_spell(spell_id=740,    cooldown=480, duration=8,  name="Tranquility",                     icon="spell_nature_tranquility.jpg", tags=[SpellTag.RAID_CD])
DRUID_RESTORATION.add_spell(spell_id=33891,  cooldown=180, duration=30, name="Incarnation: Tree of Life",       icon="ability_druid_improvedtreeform.jpg")
