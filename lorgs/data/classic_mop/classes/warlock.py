"""Define the Warlock Class and its Specs (MoP Classic)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.roles import RDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag


################################################################################
# Class
#
WARLOCK = WowClass(id=9, name="Warlock", color="#8788EE")

################################################################################
# Specs
#
WARLOCK_AFFLICTION = WowSpec(id=265, index=1, role=RDPS, wow_class=WARLOCK, name="Affliction", short_name="Aff")
WARLOCK_DEMONOLOGY = WowSpec(id=266, index=2, role=RDPS, wow_class=WARLOCK, name="Demonology", short_name="Demo")
WARLOCK_DESTRUCTION = WowSpec(id=267, index=3, role=RDPS, wow_class=WARLOCK, name="Destruction", short_name="Destro")

################################################################################
# Spells
#
WARLOCK.add_spell(spell_id=104773, cooldown=180, duration=8,  name="Unending Resolve",                icon="spell_shadow_demonictactics.jpg", show=False, tags=[SpellTag.DEFENSIVE])
WARLOCK.add_spell(spell_id=110913, cooldown=180, duration=8,  name="Dark Bargain",                    icon="ability_deathwing_bloodcorruption_death.jpg", show=False, tags=[SpellTag.DEFENSIVE])
WARLOCK.add_spell(spell_id=18540,  cooldown=600, duration=60, name="Summon Doomguard",                icon="warlock_summon_doomguard.jpg", show=False)
WARLOCK.add_spell(spell_id=1122,   cooldown=600, duration=60, name="Summon Infernal",                 icon="spell_shadow_summoninfernal.jpg", show=False)

WARLOCK_AFFLICTION.add_spell(spell_id=113860, cooldown=120, duration=20, name="Dark Soul: Misery",               icon="spell_warlock_demonsoul.jpg", tags=[SpellTag.DAMAGE])

WARLOCK_DEMONOLOGY.add_spell(spell_id=113861, cooldown=120, duration=20, name="Dark Soul: Knowledge",            icon="spell_warlock_demonsoul.jpg", tags=[SpellTag.DAMAGE])

WARLOCK_DESTRUCTION.add_spell(spell_id=113858, cooldown=120, duration=20, name="Dark Soul: Instability",          icon="spell_warlock_demonsoul.jpg", tags=[SpellTag.DAMAGE])
