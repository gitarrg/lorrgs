"""Define the Monk Class and its Specs (MoP Classic)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.roles import HEAL, MDPS, TANK
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag


################################################################################
# Class
#
MONK = WowClass(id=10, name="Monk", color="#00FF98")

################################################################################
# Specs
#
MONK_BREWMASTER = WowSpec(id=268, index=1, role=TANK, wow_class=MONK, name="Brewmaster")
MONK_MISTWEAVER = WowSpec(id=270, index=2, role=HEAL, wow_class=MONK, name="Mistweaver")
MONK_WINDWALKER = WowSpec(id=269, index=3, role=MDPS, wow_class=MONK, name="Windwalker")

################################################################################
# Spells
#
MONK.add_spell(spell_id=115203, cooldown=180, duration=20, name="Fortifying Brew",                 icon="ability_monk_fortifyingale_new.jpg", show=False, tags=[SpellTag.DEFENSIVE])
MONK.add_spell(spell_id=123904, cooldown=180, duration=45, name="Invoke Xuen, the White Tiger",    icon="ability_monk_summontigerstatue.jpg", tags=[SpellTag.DAMAGE])

MONK_BREWMASTER.add_spell(spell_id=115176, cooldown=180, duration=8,  name="Zen Meditation",                  icon="ability_monk_zenmeditation.jpg", tags=[SpellTag.TANK])
MONK_BREWMASTER.add_spell(spell_id=115213, cooldown=180, duration=6,  name="Avert Harm",                      icon="monk_ability_avertharm.jpg", tags=[SpellTag.TANK])

MONK_MISTWEAVER.add_spell(spell_id=115310, cooldown=180,              name="Revival",                         icon="spell_shaman_blessingofeternals.jpg", tags=[SpellTag.RAID_CD])
MONK_MISTWEAVER.add_spell(spell_id=116849, cooldown=120, duration=12, name="Life Cocoon",                     icon="ability_monk_chicocoon.jpg", tags=[SpellTag.RAID_CD])

MONK_WINDWALKER.add_spell(spell_id=122470, cooldown=90,  duration=10, name="Touch of Karma",                  icon="ability_monk_touchofkarma.jpg", tags=[SpellTag.DEFENSIVE])
MONK_WINDWALKER.add_spell(spell_id=115288, cooldown=60,  duration=6,  name="Energizing Brew",                 icon="ability_monk_energizingwine.jpg", show=False)
