"""Define the Hunter Class and all its Specs and Spells."""

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


################################################################################
# Class
#
HUNTER = WowClass(id=3, name="Hunter", color="#AAD372")

################################################################################
# Specs
#
HUNTER_BEASTMASTERY   = WowSpec(id=253, role=RDPS, wow_class=HUNTER,       name="Beast Mastery")
HUNTER_MARKSMANSHIP   = WowSpec(id=254, role=RDPS, wow_class=HUNTER,       name="Marksmanship")
HUNTER_SURVIVAL       = WowSpec(id=255, role=MDPS, wow_class=HUNTER,       name="Survival")

################################################################################
# Spells
#
HUNTER.add_spell(              spell_id=109304, cooldown=120,                               name="Exhilaration",        icon="ability_hunter_onewithnature.jpg", show=False, tags=[SpellTag.DEFENSIVE])
HUNTER.add_buff(               spell_id=186265, cooldown=120,                               name="Aspect of the Turtle",icon="ability_hunter_pet_turtle.jpg", show=False, tags=[SpellTag.DEFENSIVE])
HUNTER.add_spell(              spell_id=264735, cooldown=180, duration=8,                   name="Survival of the Fittest", icon="spell_nature_spiritarmor.jpg", show=False, variations=[281195], tags=[SpellTag.DEFENSIVE])
HUNTER.add_spell(              spell_id=186257, cooldown=180, duration=12, color="#F5D833", name="Aspect of the Cheetah",        icon="ability_mount_jungletiger.jpg", show=False, tags=[SpellTag.MOVE])


HUNTER_BEASTMASTERY.add_spell( spell_id=19574,  cooldown=30,  duration=15, color="#e6960f", name="Bestial Wrath",       icon="ability_druid_ferociousbite.jpg",        show=False)


HUNTER_MARKSMANSHIP.add_buff( spell_id=288613, cooldown=120,                                name="Trueshot",            icon="ability_trueshot.jpg", tags=[SpellTag.DAMAGE])
HUNTER_MARKSMANSHIP.add_spell( spell_id=260243, cooldown=45,  duration=6, color="#bf8686",  name="Volley",              icon="ability_hunter_rapidkilling.jpg", show=False)


HUNTER_SURVIVAL.add_spell(     spell_id=1250646, cooldown=90, duration=8, color="hsl(25, 60%, 50%)", name="Takedown", icon="inv12_ability_hunter_takedown.jpg")
HUNTER_SURVIVAL.add_spell(     spell_id=1261193, cooldown=60, duration=3, color="hsl(40, 40%, 70%)", name="Boomstick", icon="inv_musket_04.jpg")
HUNTER_SURVIVAL.add_spell(     spell_id=186289, cooldown=90,  duration=15,                  name="Aspect of the Eagle", icon="spell_hunter_aspectoftheironhawk.jpg", show=False)
