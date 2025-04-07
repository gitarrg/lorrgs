"""Define the Shaman Class its Specs and Spells."""

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
SHAMAN = WowClass(id=7, name="Shaman", color="#0070DD")

################################################################################
# Specs
#
SHAMAN_ELEMENTAL   = WowSpec(role=RDPS, wow_class=SHAMAN, name="Elemental")
SHAMAN_ENHANCEMENT = WowSpec(role=MDPS, wow_class=SHAMAN, name="Enhancement")
SHAMAN_RESTORATION = WowSpec(role=HEAL, wow_class=SHAMAN, name="Restoration",   short_name="Resto")

################################################################################
# Spells
#
# SHAMAN.add_spell(              spell_id=320674, cooldown=90,               color=COL_VENTR, name="Chain Harvest",              icon="ability_revendreth_shaman.jpg",             show=False)
# SHAMAN.add_spell(              spell_id=328923, cooldown=120, duration=3,  color=COL_NF,    name="Fae Transfusion",            icon="ability_ardenweald_shaman.jpg",             show=True)
SHAMAN.add_spell(              spell_id=375982, cooldown=45,               color=COL_NECRO, name="Primordial Wave",            icon="ability_maldraxxus_shaman.jpg",             show=False)

# Utils
SHAMAN.add_spell(              spell_id=108281, cooldown=120, duration=10,                  name="Ancestral Guidance",         icon="ability_shaman_ancestralguidance.jpg",      show=False, tags=[SpellTag.RAID_CD])
SHAMAN.add_spell(              spell_id=192077, cooldown=120, duration=15,                  name="Windrush Totem",             icon="ability_shaman_windwalktotem.jpg",          show=False, tags=[SpellTag.MOVE])
SHAMAN.add_spell(              spell_id=108285, cooldown=180,                               name="Totemic Recall",             icon="ability_shaman_multitotemactivation.jpg",   show=False)
SHAMAN.add_spell(              spell_id=79206,  cooldown=120, duration=15,                  name="Spiritwalker's Grace",       icon="spell_shaman_spiritwalkersgrace.jpg",       show=False, tags=[SpellTag.MOVE])

# Defensives
SHAMAN.add_spell(              spell_id=21169,                                              name="Reincarnation",              icon="spell_shaman_improvedreincarnation.jpg",    show=False, tags=[SpellTag.DEFENSIVE])
SHAMAN.add_spell(              spell_id=108271, cooldown=90,  duration=12,                  name="Astral Shift",               icon="ability_shaman_astralshift.jpg",            show=False, tags=[SpellTag.DEFENSIVE])
SHAMAN.add_buff(               spell_id=381755, cooldown=300,              color="#e0a757", name="Earth Elemental",          icon="spell_nature_earthelemental_totem.jpg",     show=False, tags=[SpellTag.DEFENSIVE])  # Buff = HP Increase from Earth Ele
SHAMAN.add_spell(              spell_id=108270, cooldown=180, duration=30, color="#e27739", name="Stone Bulwark Totem",      icon="ability_shaman_stonebulwark.jpg",           show=False, tags=[SpellTag.DEFENSIVE])


# Offensive
SHAMAN_ELEMENTAL.add_spell(    spell_id=191634, cooldown=60,               color="#00bfff", name="Stormkeeper",                icon="ability_thunderking_lightningwhip.jpg")
SHAMAN_ELEMENTAL.add_buff(     spell_id=188592, cooldown=150, duration=30, color="#ffa500", name="Fire Elemental",             icon="spell_fire_elemental_totem.jpg", tags=[SpellTag.DAMAGE])
# Note: need to track Storm Ele via Buff... but can't find a log right now.
SHAMAN_ELEMENTAL.add_spell(    spell_id=192249, cooldown=150, duration=30, color="#64b8d9", name="Storm Elemental",            icon="inv_stormelemental.jpg", tags=[SpellTag.DAMAGE])
SHAMAN_ELEMENTAL.add_spell(    spell_id=108281, cooldown=120, duration=10, color="#64b8d9", name="Ancestral Guidance",         icon="ability_shaman_ancestralguidance.jpg", tags=[SpellTag.RAID_CD], show=False)
SHAMAN_ELEMENTAL.add_buff(     spell_id=1219480,                           color="#ffcb6b", name="Ascendance",                 icon="spell_fire_elementaldevastation.jpg", tags=[SpellTag.DAMAGE])  # The Buff
SHAMAN_ELEMENTAL.add_spell(    spell_id=192222, cooldown=60,  duration=6,  color="#d15a5a", name="Liquid Magma Totem",         icon="spell_shaman_spewlava.jpg")


SHAMAN_ENHANCEMENT.add_spell(  spell_id=51533,  cooldown=120,                               name="Feral Spirit",               icon="spell_shaman_feralspirit.jpg", show=False)
SHAMAN_ENHANCEMENT.add_buff(   spell_id=384352, cooldown=60,  duration=8,  color="#42bff5", name="Doom Winds",                 icon="ability_ironmaidens_swirlingvortex.jpg")
SHAMAN_ENHANCEMENT.add_buff(   spell_id=114051, cooldown=180,              color="#ffcb6b", name="Ascendance",                 icon="spell_fire_elementaldevastation.jpg", tags=[SpellTag.DAMAGE])  # The Buff


SHAMAN_RESTORATION.add_spell(  spell_id=108280, cooldown=180, duration=10,                  name="Healing Tide Totem",         icon="ability_shaman_healingtide.jpg", tags=[SpellTag.RAID_CD])
SHAMAN_RESTORATION.add_spell(  spell_id=98008,  cooldown=180, duration=6,  color="#24b385", name="Spirit Link Totem",          icon="spell_shaman_spiritlink.jpg", tags=[SpellTag.RAID_CD])
SHAMAN_RESTORATION.add_spell(  spell_id=16191,  cooldown=180, duration=8,  color=COL_MANA,  name="Mana Tide Totem",            icon="spell_frost_summonwaterelemental.jpg",      show=False, tags=[SpellTag.RAID_CD])
SHAMAN_RESTORATION.add_spell(  spell_id=207399, cooldown=300, duration=30, color="#d15a5a", name="Ancestral Protection Totem", icon="spell_nature_reincarnation.jpg", tags=[SpellTag.RAID_CD])
SHAMAN_RESTORATION.add_spell(  spell_id=198838, cooldown=60,  duration=15, color="#a47ea6", name="Earthen Wall Totem",         icon="spell_nature_stoneskintotem.jpg",           show=False)
SHAMAN_RESTORATION.add_spell(  spell_id=157153, cooldown=30,  duration=15, color="#96d0eb", name="Cloudburst Totem",           icon="ability_shaman_condensationtotem.jpg",      show=False)
SHAMAN_RESTORATION.add_spell(  spell_id=5394,   cooldown=30,  duration=15, color="#96d0eb", name="Healing Stream Totem",       icon="inv_spear_04.jpg",      show=False)


SHAMAN_RESTORATION.add_buff(   spell_id=114052, cooldown=180,                  color="#ffcb6b", name="Ascendance",                 icon="spell_fire_elementaldevastation.jpg", tags=[SpellTag.RAID_CD])
SHAMAN_RESTORATION.add_buff(   spell_id=378270,                                color="#ffcb6b", name="Ascendance (DRE Proc)",      icon="inv_misc_herb_liferoot_stem.jpg", query=False, show=False)


def split_ascendance_procs(actor: warcraftlogs_actor.BaseActor, status: str):
    if status != "success":
        return
    if not actor:
        return
    
    for cast in actor.casts:
        if cast.spell_id == 114052 and cast.duration and cast.duration < 10_000: # real = 15sec / procs = 6sec
            cast.spell_id = 378270

warcraftlogs_actor.BaseActor.event_actor_load.connect(split_ascendance_procs)
