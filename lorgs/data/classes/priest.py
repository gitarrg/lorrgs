# """Define the Priest Class and all its Specs and Spells."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.roles import HEAL, RDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag


########################################################################################################################
# Class
#
PRIEST = WowClass(id=5, name="Priest", color="#FFFFFF")

########################################################################################################################
# Specs
#
PRIEST_DISCIPLINE = WowSpec(id=256, role=HEAL, wow_class=PRIEST, name="Discipline", short_name="Disc")
PRIEST_HOLY       = WowSpec(id=257, role=HEAL, wow_class=PRIEST, name="Holy")
PRIEST_SHADOW     = WowSpec(id=258, role=RDPS, wow_class=PRIEST, name="Shadow")

################################################################################
# Class
#
PRIEST.add_spell(              spell_id=32375,  cooldown=120,              color="#5f55f1", name="Mass Dispel",        icon="spell_arcane_massdispel.jpg", show=False)
PRIEST.add_spell(              spell_id=73325,  cooldown=90,               color="#55daf1", name="Leap of Faith",        icon="priest_spell_leapoffaith_a.jpg", show=False, tags=[SpellTag.MOVE])


# Defensive
PRIEST.add_spell(              spell_id=19236, cooldown=90,  duration=10,     name="Desperate Prayer",         icon="spell_holy_testoffaith.jpg", show=False, tags=[SpellTag.DEFENSIVE])
PRIEST.add_spell(              spell_id=586,   cooldown=30,  duration=5,      name="Fade",                     icon="spell_magic_lesserinvisibilty.jpg", show=False, tags=[SpellTag.DEFENSIVE])

PRIEST_DISCIPLINE.add_spell(   spell_id=62618,  cooldown=180, duration=10, color="#b3ad91", name="Power Word: Barrier",   icon="spell_holy_powerwordbarrier.jpg",   tags=[SpellTag.RAID_CD])
PRIEST_DISCIPLINE.add_spell(   spell_id=472433, cooldown=90,                                  name="Evangelism",            icon="spell_holy_divineillumination.jpg", tags=[SpellTag.RAID_CD])
PRIEST_DISCIPLINE.add_spell(   spell_id=194509, cooldown=20,               color="#edbb2f", name="Power Word: Radiance",  icon="spell_priest_power-word.jpg",       show=False)
PRIEST_DISCIPLINE.add_spell(   spell_id=421453, cooldown=240, duration=6,  color="#aed61d", name="Ultimate Penitence",    icon="ability_priest_ascendance.jpg",     tags=[SpellTag.RAID_CD])

PRIEST_HOLY.add_spell(         spell_id=64843,  cooldown=180, duration=8, color="#d7abdb",  name="Divine Hymn",           icon="spell_holy_divinehymn.jpg", tags=[SpellTag.RAID_CD])
PRIEST_HOLY.add_spell(         spell_id=200183, cooldown=120, duration=20,                  name="Apotheosis",            icon="ability_priest_ascension.jpg",    show=False, tags=[SpellTag.RAID_CD])
PRIEST_HOLY.add_buff(          spell_id=27827,                             color="#82eeff", name="Spirit of Redemption",  icon="inv_enchant_essenceeternallarge.jpg",    show=True)

PRIEST_SHADOW.add_spell(       spell_id=228260, cooldown=120, duration=15, color="#b330e3", name="Voidform",              icon="spell_priest_void-blast.jpg", tags=[SpellTag.DAMAGE])  # tooltip: 228264
PRIEST_SHADOW.add_spell(       spell_id=263165, cooldown=30,  duration=3,                   name="Void Torrent",          icon="spell_priest_voidsear.jpg",       show=False)
PRIEST_SHADOW.add_spell(       spell_id=47585,  cooldown=120, duration=6,                   name="Dispersion",            icon="spell_shadow_dispersion.jpg",    show=False)
PRIEST_SHADOW.add_spell(       spell_id=15286,  cooldown=120, duration=15, color="#446fc7", name="Vampiric Embrace",      icon="spell_shadow_unsummonbuilding.jpg",    show=False, tags=[SpellTag.RAID_CD])
PRIEST_SHADOW.add_spell(       spell_id=120644, cooldown=60,                                  name="Halo",                   icon="ability_priest_halo_shadow.jpg", show=False)
