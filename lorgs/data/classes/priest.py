"""Define the Priest Class and all its Specs and Spells."""

# pylint: disable=line-too-long
# pylint: disable=bad-whitespace
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.constants import *
from lorgs.data.roles import *
from lorgs.models import warcraftlogs_actor
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
PRIEST_DISCIPLINE = WowSpec(role=HEAL, wow_class=PRIEST, name="Discipline", short_name="Disc")
PRIEST_HOLY       = WowSpec(role=HEAL, wow_class=PRIEST, name="Holy")
PRIEST_SHADOW     = WowSpec(role=RDPS, wow_class=PRIEST, name="Shadow")

################################################################################
# Class
#
# PRIEST.add_spell(              spell_id=325013, cooldown=180, duration=10, color=COL_KYR,   name="Boon of the Ascended",  icon="ability_bastion_priest.jpg")
# PRIEST.add_spell(              spell_id=324724, cooldown=60,               color=COL_NECRO, name="Unholy Nova",           icon="ability_maldraxxus_priest.jpg")
# PRIEST.add_spell(              spell_id=323673, cooldown=45,  duration=5,  color=COL_VENTR, name="Mindgames",             icon="ability_revendreth_priest.jpg")
PRIEST.add_spell(              spell_id=32375,  cooldown=120,              color="#5f55f1", name="Mass Dispel",        icon="spell_arcane_massdispel.jpg", show=False)
PRIEST.add_spell(              spell_id=73325,  cooldown=90,               color="#55daf1", name="Leap of Faith",        icon="priest_spell_leapoffaith_a.jpg", show=False, tags=[SpellTag.MOVE])
PRIEST.add_spell(              spell_id=120517, cooldown=60,                                  name="Halo",                   icon="ability_priest_halo.jpg", show=False, variations=[120644])

PRIEST.add_spell(
    spell_id=428924, cooldown=60,
    name="Premonition", icon="inv_ability_oraclepriest_premonitioninsight.jpg",
    show=False,
    variations=[
        428933,  # Premonition of Insight
        428930,  # Premonition of Piety
        428934,  # Premonition of Solace
        440725,  # Premonition of Clairvoyance
    ]
)



# Defensive
PRIEST.add_spell(              spell_id=19236, cooldown=90,  duration=10,     name="Desperate Prayer",         icon="spell_holy_testoffaith.jpg", show=False, tags=[SpellTag.DEFENSIVE])
PRIEST.add_spell(              spell_id=586,   cooldown=30,  duration=5,      name="Fade",                     icon="spell_magic_lesserinvisibilty.jpg", show=False, tags=[SpellTag.DEFENSIVE])

# Offensive
PRIEST_DISCIPLINE.add_spell(   spell_id=62618,  cooldown=180, duration=10, color="#b3ad91", name="Power Word: Barrier",   icon="spell_holy_powerwordbarrier.jpg", tags=[SpellTag.RAID_CD])
PRIEST_DISCIPLINE.add_spell(   spell_id=271466, cooldown=180, duration=10, color="#b3ad91", name="Luminous Barrier",      icon="spell_priest_burningwill.jpg", tags=[SpellTag.RAID_CD])
# PRIEST_DISCIPLINE.add_spell(   spell_id=109964, cooldown=60,  duration=10, color="#d7abdb", name="Spirit Shell",          icon="ability_shaman_astralshift.jpg", tags=[SpellTag.RAID_CD])
PRIEST_DISCIPLINE.add_spell(   spell_id=47536,  cooldown=90,  duration=8,                   name="Rapture",               icon="spell_holy_rapture.jpg",          show=True, tags=[SpellTag.RAID_CD])
PRIEST_DISCIPLINE.add_spell(   spell_id=472433, cooldown=90,                                name="Evangelism",            icon="spell_holy_divineillumination.jpg", tags=[SpellTag.RAID_CD])
PRIEST_DISCIPLINE.add_spell(   spell_id=194509, cooldown=20,               color="#edbb2f", name="Power Word: Radiance",  icon="spell_priest_power-word.jpg",     show=False)
PRIEST_DISCIPLINE.add_spell(   spell_id=314867, cooldown=30, duration=7,   color="#6633cc", name="Shadow Covenant",       icon="spell_shadow_summonvoidwalker.jpg", show=False)
PRIEST_DISCIPLINE.add_spell(   spell_id=373178, cooldown=90,               color="#e85465", name="Light's Wrath",         icon="inv_staff_2h_artifacttome_d_01.jpg", show=False)
PRIEST_DISCIPLINE.add_spell(   spell_id=421453, cooldown=240, duration=6,  color="#aed61d", name="Ultimate Penitence",         icon="ability_priest_ascendance.jpg", tags=[SpellTag.RAID_CD])

PRIEST_HOLY.add_spell(         spell_id=64843,  cooldown=180, duration=8, color="#d7abdb",  name="Divine Hymn",           icon="spell_holy_divinehymn.jpg", tags=[SpellTag.RAID_CD])
PRIEST_HOLY.add_spell(         spell_id=265202, cooldown=240,                               name="Holy Word: Salvation",  icon="ability_priest_archangel.jpg",    tags=[SpellTag.DYNAMIC_CD, SpellTag.RAID_CD])
PRIEST_HOLY.add_spell(         spell_id=200183, cooldown=120, duration=20,                  name="Apotheosis",            icon="ability_priest_ascension.jpg",    show=False)
PRIEST_HOLY.add_buff(          spell_id=27827,                             color="#82eeff", name="Spirit of Redemption",  icon="inv_enchant_essenceeternallarge.jpg",    show=True)
PRIEST_HOLY.add_spell(         spell_id=64901, cooldown=180, duration=5,   color="#4dd196", name="Symbol of Hope",        icon="spell_holy_symbolofhope.jpg",    show=False, tags=[SpellTag.RAID_CD])
PRIEST_HOLY.add_spell(         spell_id=372835, cooldown=120,              color="#edbb2f", name="Lightwell",             icon="spell_holy_summonlightwell.jpg",    show=False, tags=[SpellTag.RAID_CD])

PRIEST_SHADOW.add_spell(       spell_id=228260, cooldown=120, duration=15, color="#b330e3", name="Voidform",              icon="spell_priest_void-blast.jpg", tags=[SpellTag.DAMAGE])  # tooltip: 228264
PRIEST_SHADOW.add_spell(       spell_id=391109, cooldown=60,  duration=20, color="#308fbf", name="Dark Ascension",        icon="ability_priest_darkarchangel.jpg", tags=[SpellTag.DAMAGE])
PRIEST_SHADOW.add_spell(       spell_id=263165, cooldown=30,  duration=3,                   name="Void Torrent",          icon="spell_priest_voidsear.jpg",       show=False)
PRIEST_SHADOW.add_spell(       spell_id=47585,  cooldown=120, duration=6,                   name="Dispersion",            icon="spell_shadow_dispersion.jpg",    show=False)
PRIEST_SHADOW.add_spell(       spell_id=15286,  cooldown=120, duration=15, color="#446fc7", name="Vampiric Embrace",      icon="spell_shadow_unsummonbuilding.jpg",    show=False, tags=[SpellTag.RAID_CD])
# 11.1 T Set (Random PI Procs)
SHADOW_JACKPOT = PRIEST_SHADOW.add_spell(       spell_id=1215703,duration=4,                color="#f7c625", name="Jackpot!",              icon="spell_holy_powerinfusion.jpg",    show=False)


# Shadowfiend/Mindbeder Variations (with different glyphs etc)
for spec in (PRIEST_SHADOW, PRIEST_DISCIPLINE):
    spec.add_spell(spell_id=123040, cooldown=60,  duration=15, color="#58db97", name="Mindbender", icon="spell_shadow_soulleech_3.jpg", variations=[200174])
    spec.add_spell(spell_id=132603, cooldown=180, duration=15, color="#58db97", name="Shadowfiend", icon="spell_shadow_shadowfiend.jpg", variations=[34433, 254232, 254224])
    spec.add_spell(spell_id=451235, cooldown=60,  duration=15, color="#58db97", name="Voidwraith", icon="warlock_curse_shadow.jpg")


def filter_pi_procs(actor: warcraftlogs_actor.BaseActor, status: str):
    if status != "success":
        return
    if not actor:
        return
    
    for cast in actor.casts:
        if cast.duration and cast.spell_id == 10060 and cast.duration < 19_000:
            cast.spell_id = SHADOW_JACKPOT.spell_id

warcraftlogs_actor.BaseActor.event_actor_load.connect(filter_pi_procs)
