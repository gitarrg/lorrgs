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
HUNTER_BEASTMASTERY   = WowSpec(role=RDPS, wow_class=HUNTER,       name="Beast Mastery")
HUNTER_MARKSMANSHIP   = WowSpec(role=RDPS, wow_class=HUNTER,       name="Marksmanship")
HUNTER_SURVIVAL       = WowSpec(role=MDPS, wow_class=HUNTER,       name="Survival")

################################################################################
# Spells
#
HUNTER.add_spell(              spell_id=328231, cooldown=120, duration=15, color=COL_NF,    name="Wild Spirits",        icon="ability_ardenweald_hunter.jpg")
HUNTER.add_spell(              spell_id=308491, cooldown=60,  duration=10, color=COL_KYR,   name="Resonating Arrow",    icon="ability_bastion_hunter.jpg")
HUNTER.add_spell(              spell_id=375891, cooldown=45,  duration=10, color=COL_NECRO, name="Death Chakram",    icon="ability_maldraxxus_hunter.jpg")


HUNTER.add_spell(              spell_id=109304, cooldown=120,                               name="Exhilaration",        icon="ability_hunter_onewithnature.jpg", show=False, tags=[SpellTag.DEFENSIVE])
HUNTER.add_buff(               spell_id=186265, cooldown=120,                               name="Aspect of the Turtle",icon="ability_hunter_pet_turtle.jpg", show=False, tags=[SpellTag.DEFENSIVE])
HUNTER.add_spell(              spell_id=264735, cooldown=180, duration=8,                   name="Survival of the Fittest", icon="spell_nature_spiritarmor.jpg", show=False, variations=[281195], tags=[SpellTag.DEFENSIVE])
HUNTER.add_buff(               spell_id=339461, cooldown=30,                                name="Resilience of the Hunter",icon="ability_rogue_feigndeath.jpg", show=False, tags=[SpellTag.DEFENSIVE])
HUNTER.add_spell(              spell_id=212431, cooldown=30,                                name="Explosive Shot",icon="ability_hunter_explosiveshot.jpg", show=False)


HUNTER_BEASTMASTERY.add_spell( spell_id=193530, cooldown=180, duration=20,                  name="Aspect of the Wild",  icon="spell_nature_protectionformnature.jpg", tags=[SpellTag.DAMAGE])
HUNTER_BEASTMASTERY.add_spell( spell_id=19574,  cooldown=30,  duration=15, color="#e6960f", name="Bestial Wrath",       icon="ability_druid_ferociousbite.jpg",        show=False)
HUNTER_BEASTMASTERY.add_spell( spell_id=321530, cooldown=60,  duration=18, color="#b34747", name="Bloodshed",           icon="ability_druid_primaltenacity.jpg")
HUNTER_BEASTMASTERY.add_spell( spell_id=272679, cooldown=120, duration=10,                  name="Fortitude of the Bear", icon="spell_druid_bearhug.jpg", show=False)
HUNTER_BEASTMASTERY.add_spell( spell_id=359844, cooldown=120, duration=20,                  name="Call of the Wild", icon="ability_hunter_callofthewild.jpg", tags=[SpellTag.DAMAGE])


HUNTER_MARKSMANSHIP.add_buff( spell_id=288613, cooldown=120,                                name="Trueshot",            icon="ability_trueshot.jpg", tags=[SpellTag.DAMAGE])
HUNTER_MARKSMANSHIP.add_buff( spell_id=378905,                                              name="Windrunner's Guidance", icon="ability_hunter_laceration.jpg", show=False, query=True)
HUNTER_MARKSMANSHIP.add_spell( spell_id=260243, cooldown=45,  duration=6, color="#bf8686",  name="Volley",              icon="ability_hunter_rapidkilling.jpg", show=False)

HUNTER_SURVIVAL.add_spell(     spell_id=360952, cooldown=120, duration=20,                  name="Coordinated Assault", icon="inv_coordinatedassault.jpg", tags=[SpellTag.DAMAGE])
HUNTER_SURVIVAL.add_spell(     spell_id=186289, cooldown=90,  duration=15,                  name="Aspect of the Eagle", icon="spell_hunter_aspectoftheironhawk.jpg")
HUNTER_SURVIVAL.add_spell(     spell_id=360966, cooldown=90,  duration=12, color="#3aa65e", name="Spearhead",           icon="ability_hunter_spearhead.jpg")
HUNTER_SURVIVAL.add_spell(     spell_id=203415, cooldown=45,  duration=4,  color="#3a96a6", name="Fury of the Eagle", icon="inv_polearm_2h_artifacteagle_d_01.jpg")


def split_trueshot_procs(actor: warcraftlogs_actor.BaseActor, status: str):
    if status != "success":
        return
    if not actor:
        return
    
    for cast in actor.casts:
        if cast.spell_id == 288613 and cast.duration and cast.duration < 14_000:
            cast.spell_id = 378905

warcraftlogs_actor.BaseActor.event_actor_load.connect(split_trueshot_procs)
