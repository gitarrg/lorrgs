"""Define the Rogue Class and its Specs (MoP Classic)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.roles import MDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag


################################################################################
# Class
#
ROGUE = WowClass(id=4, name="Rogue", color="#FFF468")

################################################################################
# Specs
#
ROGUE_ASSASSINATION = WowSpec(id=259, index=1, role=MDPS, wow_class=ROGUE, name="Assassination", short_name="Assa")
ROGUE_COMBAT = WowSpec(id=260, index=2, role=MDPS, wow_class=ROGUE, name="Combat")
ROGUE_SUBTLETY = WowSpec(id=261, index=3, role=MDPS, wow_class=ROGUE, name="Subtlety")

################################################################################
# Spells
#
ROGUE.add_spell(spell_id=121471, cooldown=180, duration=12, name="Shadow Blades",                   icon="inv_knife_1h_grimbatolraid_d_03.jpg", tags=[SpellTag.DAMAGE])
ROGUE.add_spell(spell_id=1856,   cooldown=120, duration=3,  name="Vanish",                          icon="ability_vanish.jpg", show=False)
ROGUE.add_spell(spell_id=5277,   cooldown=120, duration=10, name="Evasion",                         icon="spell_shadow_shadowward.jpg", show=False, tags=[SpellTag.DEFENSIVE])
ROGUE.add_spell(spell_id=76577,  cooldown=180, duration=5,  name="Smoke Bomb",                      icon="ability_rogue_smoke.jpg", show=False, tags=[SpellTag.RAID_CD])
ROGUE.add_spell(spell_id=114018, cooldown=300, duration=15, name="Shroud of Concealment",           icon="ability_rogue_shroudofconcealment.jpg", show=False)

ROGUE_ASSASSINATION.add_spell(spell_id=79140,  cooldown=120, duration=20, name="Vendetta",                        icon="ability_rogue_deadliness.jpg", tags=[SpellTag.DAMAGE])

ROGUE_COMBAT.add_spell(spell_id=51690,  cooldown=120, duration=3.5,name="Killing Spree",                   icon="ability_rogue_murderspree.jpg", tags=[SpellTag.DAMAGE])
ROGUE_COMBAT.add_spell(spell_id=13750,  cooldown=180, duration=15, name="Adrenaline Rush",                 icon="spell_shadow_shadowworddominate.jpg", tags=[SpellTag.DAMAGE])

ROGUE_SUBTLETY.add_spell(spell_id=51713,  cooldown=60,  duration=8,  name="Shadow Dance",                    icon="ability_rogue_shadowdance.jpg", tags=[SpellTag.DAMAGE])
ROGUE_SUBTLETY.add_spell(spell_id=14185,  cooldown=300,              name="Preparation",                     icon="ability_rogue_preparation.jpg", show=False)
