"""Define the Warlock Class its Specs and Spells."""

# pylint: disable=line-too-long
# pylint: disable=bad-whitespace
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.constants import *
from lorgs.data.roles import RDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag, WowSpell


################################################################################
# Class
#
WARLOCK = WowClass(id=9, name="Warlock", color="#8788EE")

################################################################################
# Specs
#
WARLOCK_AFFLICTION  = WowSpec(id=265, role=RDPS, wow_class=WARLOCK, name="Affliction",  short_name="Aff")
WARLOCK_DEMONOLOGY  = WowSpec(id=266, role=RDPS, wow_class=WARLOCK, name="Demonology",  short_name="Demo")
WARLOCK_DESTRUCTION = WowSpec(id=267, role=RDPS, wow_class=WARLOCK, name="Destruction", short_name="Destro")

################################################################################
# Spells
#
WARLOCK.add_spell(             spell_id=104773, cooldown=300, duration=8,                   name="Unending Resolve",       icon="spell_shadow_demonictactics.jpg", show=False, tags=[SpellTag.DEFENSIVE])
WARLOCK.add_buff(              spell_id=108416, cooldown=60,                                name="Dark Pact",              icon="spell_shadow_deathpact.jpg",      show=False, tags=[SpellTag.DEFENSIVE]) # auto duration
WARLOCK.add_spell(             spell_id=452930, cooldown=60, duration=6,   color="#cc5252", name="Demonic Healthstone",  icon="warlock_-bloodstone.jpg",         show=False, tags=[SpellTag.DEFENSIVE])

WARLOCK_AFFLICTION.add_spell(  spell_id=205180, cooldown=120, duration=8,  color="#49ad6e", name="Summon Darkglare",       icon="inv_beholderwarlock.jpg", tags=[SpellTag.DAMAGE])
WARLOCK_AFFLICTION.add_spell(  spell_id=1257052, cooldown=60, duration=3,  color="#c35ec4", name="Dark Harvest",             icon="inv_ability_warlock_soulrot.jpg", show=False)


WARLOCK_DEMONOLOGY.add_spell(  spell_id=265187,  cooldown=60,  duration=15, color="#9150ad", name="Summon Demonic Tyrant",  icon="inv_summondemonictyrant.jpg", tags=[SpellTag.DAMAGE])
WARLOCK_DEMONOLOGY.add_spell(  spell_id=1276672, cooldown=120, duration=12, color="#d9a336", name="Summon Doomguard",       icon="warlock_summon_doomguard.jpg", tags=[SpellTag.DAMAGE])
WARLOCK_DEMONOLOGY.add_spell(  spell_id=1276452, cooldown=120, duration=20, color="#43964a", name="Grimoire: Imp Lord",     icon="inv_imp3_purple.jpg")
WARLOCK_DEMONOLOGY.add_spell(  spell_id=1276467, cooldown=120, duration=20, color="#c46837", name="Grimoire: Fel Ravager",  icon="spell_shadow_summonfelhunter.jpg")

WARLOCK_DESTRUCTION.add_spell( spell_id=1122,   cooldown=180, duration=30, color="#91c45a", name="Summon Infernal",        icon="spell_shadow_summoninfernal.jpg", tags=[SpellTag.DAMAGE])
WARLOCK_DESTRUCTION.add_spell( spell_id=80240,  cooldown=30,  duration=12, color="#cc5252", name="Havoc",                  icon="ability_warlock_baneofhavoc.jpg", show=False)


# Additional Spells (not tracked)
SOULSTONE_RESURRECTION = WowSpell(spell_id=95750, name="Soulstone", icon="spell_shadow_soulgem.jpg")


################################################################################
# Hero Talents

Malevolence = WowSpell(
    spell_id=442726, name="Malevolence",
    cooldown=60, duration=20, color="#8048cf",
    icon="inv_ability_hellcallerwarlock_malevolence.jpg",
    show=True,
    spell_type=WARLOCK.name_slug,
)
WARLOCK_AFFLICTION.add_spell(Malevolence)
WARLOCK_DESTRUCTION.add_spell(Malevolence)
