"""Define the Hunter Class and its Specs (MoP Classic)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.roles import RDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag


################################################################################
# Class
#
HUNTER = WowClass(id=3, name="Hunter", color="#AAD372")

################################################################################
# Specs
#
HUNTER_BEASTMASTERY = WowSpec(id=253, index=1, role=RDPS, wow_class=HUNTER, name="Beast Mastery")
HUNTER_MARKSMANSHIP = WowSpec(id=254, index=2, role=RDPS, wow_class=HUNTER, name="Marksmanship")
HUNTER_SURVIVAL = WowSpec(id=255, index=3, role=RDPS, wow_class=HUNTER, name="Survival")

################################################################################
# Spells
#
HUNTER.add_spell(spell_id=3045,   cooldown=180, duration=15, name="Rapid Fire",                      icon="ability_hunter_runningshot.jpg", tags=[SpellTag.DAMAGE])
HUNTER.add_spell(spell_id=121818, cooldown=300, duration=20, name="Stampede",                        icon="ability_hunter_bestialdiscipline.jpg", tags=[SpellTag.DAMAGE])
HUNTER.add_spell(spell_id=131894, cooldown=120, duration=30, name="A Murder of Crows",               icon="ability_hunter_murderofcrows.jpg", tags=[SpellTag.DAMAGE])
HUNTER.add_spell(spell_id=19263,  cooldown=180, duration=5,  name="Deterrence",                      icon="ability_whirlwind.jpg", show=False, tags=[SpellTag.DEFENSIVE])

HUNTER_BEASTMASTERY.add_spell(spell_id=19574,  cooldown=60,  duration=10, name="Bestial Wrath",                   icon="ability_druid_ferociousbite.jpg", tags=[SpellTag.DAMAGE])
