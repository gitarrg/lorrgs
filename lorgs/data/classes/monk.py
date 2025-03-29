"""Define the Monk Class and all its Specs and Spells."""

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
MONK_BREWMASTER = WowSpec(role=TANK, wow_class=MONK, name="Brewmaster")
MONK_MISTWEAVER = WowSpec(role=HEAL, wow_class=MONK, name="Mistweaver")
MONK_WINDWALKER = WowSpec(role=MDPS, wow_class=MONK, name="Windwalker")

################################################################################
# Spells
#
MONK.add_spell(           spell_id=387184, cooldown=120, duration=30, color=COL_KYR,   name="Weapons of Order",                icon="ability_bastion_monk.jpg",            show=False)
MONK.add_spell(           spell_id=386276, cooldown=60,  duration=10, color=COL_NECRO, name="Bonedust Brew",                   icon="ability_maldraxxus_monk.jpg",         show=False)
MONK.add_spell(           spell_id=327104, cooldown=30,  duration=30, color=COL_NF,    name="Faeline Stomp",                   icon="ability_ardenweald_monk.jpg",         show=False)


# Defensive
MONK.add_spell(spell_id=122278, cooldown=120, duration=10, color="#fcba03", name="Dampen Harm",                     icon="ability_monk_dampenharm.jpg", show=False, tags=[SpellTag.DEFENSIVE])
MONK.add_spell(spell_id=122783, cooldown=90,  duration=6,  color="#f5d142", name="Diffuse Magic", icon="spell_monk_diffusemagic.jpg", show=False, tags=[SpellTag.DEFENSIVE])
MONK.add_spell(spell_id=115203, cooldown=180, duration=15, color="#ffb145", name="Fortifying Brew", icon="ability_monk_fortifyingale_new.jpg", show=False, tags=[SpellTag.DEFENSIVE])

# Offensive
MONK.add_spell(           spell_id=322109, cooldown=180,              color="#c72649", name="Touch of Death",                  icon="ability_monk_touchofdeath.jpg")
MONK.add_spell(           spell_id=388686, cooldown=120,              color="#8dd6bf", name="Summon White Tiger Statue",       icon="ability_monk_summonwhitetigerstatue.jpg", show=False)

MONK_MISTWEAVER.add_spell(spell_id=322118, cooldown=120, duration=4.5 ,                 name="Invoke Yu'lon, the Jade Serpent", icon="ability_monk_dragonkick.jpg", tags=[SpellTag.RAID_CD])
MONK_MISTWEAVER.add_spell(spell_id=115310, cooldown=180,              color="#00FF98", name="Revival",                          icon="spell_monk_revival.jpg", tags=[SpellTag.RAID_CD], variations=[388615])
MONK_MISTWEAVER.add_spell(spell_id=325197, cooldown=120, duration=25, color="#e0bb36", name="Invoke Chi-Ji, the Red Crane",     icon="inv_pet_cranegod.jpg", tags=[SpellTag.RAID_CD])
MONK_MISTWEAVER.add_spell(spell_id=116680, cooldown=30,               color="#22a5e6", name="Thunder Focus Tea",                icon="ability_monk_thunderfocustea.jpg", show=False)
MONK_MISTWEAVER.add_spell(spell_id=399491,               duration=8,  color="#78e048", name="Sheilun's Gift",                   icon="inv_staff_2h_artifactshaohao_d_01.jpg", show=False)
MONK_MISTWEAVER.add_buff(spell_id=197908,                             color="#22a5e6", name="Mana Tea",                         icon="monk_ability_cherrymanatea.jpg", show=False)


MONK_WINDWALKER.add_spell(spell_id=123904, cooldown=120, duration=24, color="#8cdbbc", name="Invoke Xuen, the White Tiger",    icon="ability_monk_summontigerstatue.jpg", tags=[SpellTag.DAMAGE])
MONK_WINDWALKER.add_spell(spell_id=137639, cooldown=90,  duration=15, color="#be53db", name="Storm, Earth, and Fire",          icon="spell_nature_giftofthewild.jpg")
MONK_WINDWALKER.add_spell(spell_id=122470, cooldown=90,  duration=10, color="#8afbff", name="Touch of Karma",                  icon="ability_monk_touchofkarma.jpg", show=False)
MONK_WINDWALKER.add_spell(spell_id=152173, cooldown=90,  duration=12,                  name="Serenity"      ,                  icon="ability_monk_serenity.jpg", show=False)


MONK_BREWMASTER.add_spell(spell_id=322507, cooldown=60,  duration=0,  color="#45f9ff", name="Celestial Brew",                  icon="ability_monk_ironskinbrew.jpg",        show=False)
MONK_BREWMASTER.add_spell(spell_id=132578, cooldown=180, duration=25,                  name="Invoke Niuzao the Black Ox",      icon="spell_monk_brewmaster_spec.jpg", tags=[SpellTag.TANK])
MONK_BREWMASTER.add_spell(spell_id=115176, cooldown=300, duration=8,                   name="Zen Meditation",                  icon="ability_monk_zenmeditation.jpg", tags=[SpellTag.TANK])
MONK_BREWMASTER.add_spell(spell_id=115203, cooldown=360, duration=15, color="#ffb145", name="Fortifying Brew",                 icon="ability_monk_fortifyingale_new.jpg", tags=[SpellTag.DEFENSIVE])
MONK_BREWMASTER.add_spell(spell_id=325153, cooldown=60,  duration=3,  color="#cc5a89", name="Exploding Keg",                 icon="archaeology_5_0_emptykegofbrewfatherxinwoyin.jpg")


# Hero Talents
CelestialConduit = WowSpell(
    spell_id=443028, name="Celestial Conduit",
    cooldown=90, duration=4, color="#72d81e",
    icon="inv_ability_conduitofthecelestialsmonk_celestialconduit.jpg",
    show=False,
    spell_type=MONK.name_slug,
)
MONK_MISTWEAVER.add_spell(CelestialConduit)
MONK_WINDWALKER.add_spell(CelestialConduit)
