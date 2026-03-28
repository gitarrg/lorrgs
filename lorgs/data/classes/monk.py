# """Define the Monk Class and all its Specs and Spells."""

# pylint: disable=line-too-long
# pylint: disable=bad-whitespace
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.constants import *
from lorgs.data.roles import *
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag, WowSpell


################################################################################
# Class
#
MONK = WowClass(id=10, name="Monk", color="#00FF98")

################################################################################
# Specs
#
MONK_BREWMASTER = WowSpec(id=268, role=TANK, wow_class=MONK, name="Brewmaster")
MONK_MISTWEAVER = WowSpec(id=270, role=HEAL, wow_class=MONK, name="Mistweaver")
MONK_WINDWALKER = WowSpec(id=269, role=MDPS, wow_class=MONK, name="Windwalker")

################################################################################
# Spells
#

MONK.add_spell(spell_id=115203, cooldown=180, duration=15, color="#ffb145", name="Fortifying Brew", icon="ability_monk_fortifyingale_new.jpg", show=False, tags=[SpellTag.DEFENSIVE])
MONK.add_spell(           spell_id=322109, cooldown=180,              color="#c72649", name="Touch of Death",                  icon="ability_monk_touchofdeath.jpg")


MONK_MISTWEAVER.add_spell(spell_id=322118, cooldown=120, duration=4.5 ,                 name="Invoke Yu'lon, the Jade Serpent", icon="ability_monk_dragonkick.jpg", tags=[SpellTag.RAID_CD])
MONK_MISTWEAVER.add_spell(spell_id=115310, cooldown=180,              color="#00FF98", name="Revival",                          icon="spell_monk_revival.jpg", tags=[SpellTag.RAID_CD], variations=[388615])
MONK_MISTWEAVER.add_spell(spell_id=325197, cooldown=120, duration=25, color="#e0bb36", name="Invoke Chi-Ji, the Red Crane",     icon="inv_pet_cranegod.jpg", tags=[SpellTag.RAID_CD])
MONK_MISTWEAVER.add_spell(spell_id=116680, cooldown=30,               color="#22a5e6", name="Thunder Focus Tea",                icon="ability_monk_thunderfocustea.jpg", show=False)
MONK_MISTWEAVER.add_spell(spell_id=443028, cooldown=90,  duration=4,  color="#72d81e", name="Celestial Conduit",     icon="inv_ability_conduitofthecelestialsmonk_celestialconduit.jpg", show=False)


MONK_WINDWALKER.add_spell(spell_id=122470, cooldown=90,  duration=10, color="#8afbff", name="Touch of Karma",                  icon="ability_monk_touchofkarma.jpg", show=False)
MONK_WINDWALKER.add_spell(spell_id=1249625, cooldown=90,  duration=15, color="#3DC280", name="Zenith",                          icon="inv_ability_monk_weaponsoforder.jpg")


MONK_BREWMASTER.add_spell(spell_id=322507, cooldown=60,  duration=0,  color="#45f9ff", name="Celestial Brew",                  icon="ability_monk_ironskinbrew.jpg",        show=False)
MONK_BREWMASTER.add_spell(spell_id=132578, cooldown=180, duration=25,                  name="Invoke Niuzao the Black Ox",      icon="spell_monk_brewmaster_spec.jpg", tags=[SpellTag.TANK])
MONK_BREWMASTER.add_spell(spell_id=115176, cooldown=300, duration=8,                   name="Zen Meditation",                  icon="ability_monk_zenmeditation.jpg", tags=[SpellTag.TANK])
MONK_BREWMASTER.add_spell(spell_id=325153, cooldown=60,  duration=3,  color="#cc5a89", name="Exploding Keg",                 icon="archaeology_5_0_emptykegofbrewfatherxinwoyin.jpg")
MONK_BREWMASTER.add_spell(spell_id=1241059, cooldown=45,              color="#dd422d", name="Celestial Infusion",                 icon="ability_monk_tigereyebrandy.jpg")
