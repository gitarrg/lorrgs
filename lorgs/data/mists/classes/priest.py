"""Define the Priest Class and its Specs (MoP Classic)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.roles import HEAL, RDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag


################################################################################
# Class
#
PRIEST = WowClass(id=5, name="Priest", color="#FFFFFF")

################################################################################
# Specs
#
PRIEST_DISCIPLINE = WowSpec(id=256, index=1, role=HEAL, wow_class=PRIEST, name="Discipline", short_name="Disc")
PRIEST_HOLY = WowSpec(id=257, index=2, role=HEAL, wow_class=PRIEST, name="Holy")
PRIEST_SHADOW = WowSpec(id=258, index=3, role=RDPS, wow_class=PRIEST, name="Shadow")

################################################################################
# Spells
#
PRIEST.add_spell(spell_id=34433,  cooldown=180, duration=12, name="Shadowfiend",                     icon="spell_shadow_shadowfiend.jpg", tags=[SpellTag.DAMAGE])
PRIEST.add_spell(spell_id=10060,  cooldown=120, duration=20, name="Power Infusion",                  icon="spell_holy_powerinfusion.jpg", tags=[SpellTag.DAMAGE])
PRIEST.add_spell(spell_id=19236,  cooldown=120,              name="Desperate Prayer",                icon="spell_holy_testoffaith.jpg", show=False, tags=[SpellTag.DEFENSIVE])
PRIEST.add_spell(spell_id=108968, cooldown=300,              name="Void Shift",                      icon="spell_priest_voidshift.jpg", show=False)
PRIEST.add_spell(spell_id=64901,  cooldown=360, duration=8,  name="Hymn of Hope",                    icon="spell_holy_symbolofhope.jpg", show=False)

PRIEST_DISCIPLINE.add_spell(spell_id=33206,  cooldown=180, duration=8,  name="Pain Suppression",                icon="spell_holy_painsupression.jpg", tags=[SpellTag.RAID_CD])
PRIEST_DISCIPLINE.add_spell(spell_id=62618,  cooldown=180, duration=10, name="Power Word: Barrier",             icon="spell_holy_powerwordbarrier.jpg", tags=[SpellTag.RAID_CD])

PRIEST_HOLY.add_spell(spell_id=64843,  cooldown=180, duration=8,  name="Divine Hymn",                     icon="spell_holy_divinehymn.jpg", tags=[SpellTag.RAID_CD])
PRIEST_HOLY.add_spell(spell_id=47788,  cooldown=180, duration=10, name="Guardian Spirit",                 icon="spell_holy_guardianspirit.jpg", tags=[SpellTag.RAID_CD])

PRIEST_SHADOW.add_spell(spell_id=47585,  cooldown=120, duration=6,  name="Dispersion",                      icon="spell_shadow_dispersion.jpg", show=False, tags=[SpellTag.DEFENSIVE])
PRIEST_SHADOW.add_spell(spell_id=15286,  cooldown=180, duration=15, name="Vampiric Embrace",                icon="spell_shadow_unsummonbuilding.jpg", show=False, tags=[SpellTag.RAID_CD])
