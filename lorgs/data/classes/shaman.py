# """Define the Shaman Class its Specs and Spells."""

# pylint: disable=line-too-long
# pylint: disable=bad-whitespace
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.constants import *
from lorgs.data.roles import HEAL, MDPS, RDPS
from lorgs.models import warcraftlogs_actor
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag, WowSpell


################################################################################
# Class
#
SHAMAN = WowClass(id=7, name="Shaman", color="#0070DD")

################################################################################
# Specs
#
SHAMAN_ELEMENTAL   = WowSpec(id=262, role=RDPS, wow_class=SHAMAN, name="Elemental")
SHAMAN_ENHANCEMENT = WowSpec(id=263, role=MDPS, wow_class=SHAMAN, name="Enhancement")
SHAMAN_RESTORATION = WowSpec(id=264, role=HEAL, wow_class=SHAMAN, name="Restoration",   short_name="Resto")

################################################################################
# Spells
#

# Utils
SHAMAN.add_spell(              spell_id=192077, cooldown=120, duration=15,                  name="Windrush Totem",             icon="ability_shaman_windwalktotem.jpg",          show=False, tags=[SpellTag.MOVE])
SHAMAN.add_spell(              spell_id=79206,  cooldown=120, duration=15,                  name="Spiritwalker's Grace",       icon="spell_shaman_spiritwalkersgrace.jpg",       show=False, tags=[SpellTag.MOVE])

# Defensives
SHAMAN.add_spell(              spell_id=21169,                                              name="Reincarnation",              icon="spell_shaman_improvedreincarnation.jpg",    show=False, tags=[SpellTag.DEFENSIVE])
SHAMAN.add_spell(              spell_id=108271, cooldown=90,  duration=12,                  name="Astral Shift",               icon="ability_shaman_astralshift.jpg",            show=False, tags=[SpellTag.DEFENSIVE])
SHAMAN.add_buff(               spell_id=381755, cooldown=300,              color="#e0a757", name="Earth Elemental",          icon="spell_nature_earthelemental_totem.jpg",     show=False, tags=[SpellTag.DEFENSIVE], wowhead_data="spell=198103")  # Buff = HP Increase from Earth Ele


# Offensive
SHAMAN_ELEMENTAL.add_spell(    spell_id=191634, cooldown=60,               color="#00bfff", name="Stormkeeper",                icon="ability_thunderking_lightningwhip.jpg")
SHAMAN_ELEMENTAL.add_spell(    spell_id=114050,               duration=15, color="#ffcb6b", name="Ascendance",                 icon="spell_fire_elementaldevastation.jpg", tags=[SpellTag.DAMAGE])


SHAMAN_ENHANCEMENT.add_spell(  spell_id=384352, cooldown=60,  duration=8,  color="#42bff5", name="Doom Winds",                 icon="ability_ironmaidens_swirlingvortex.jpg")
SHAMAN_ENHANCEMENT.add_spell(  spell_id=114051, cooldown=10, duration=15, color="#ffcb6b", name="Ascendance",                 icon="spell_fire_elementaldevastation.jpg", tags=[SpellTag.DAMAGE])


SHAMAN_RESTORATION.add_spell(  spell_id=108280, cooldown=180, duration=10,                    name="Healing Tide Totem",         icon="ability_shaman_healingtide.jpg", tags=[SpellTag.RAID_CD])
SHAMAN_RESTORATION.add_spell(  spell_id=98008,  cooldown=180, duration=6,  color="#24b385", name="Spirit Link Totem",          icon="spell_shaman_spiritlink.jpg", tags=[SpellTag.RAID_CD])
RESTO_ASCENDANCE = SHAMAN_RESTORATION.add_spell(spell_id=114052, cooldown=180, duration=30, color="#ffcb6b", name="Ascendance", icon="spell_fire_elementaldevastation.jpg", tags=[SpellTag.RAID_CD])

# we need to query both: casts and buffs to be able to split DRE procs
DRE = SHAMAN_RESTORATION.add_buff(spell_id=378270, color="#ffcb6b", name="Deeply Rooted Elements", icon="inv_misc_herb_liferoot_stem.jpg", show=False, query=False)
SHAMAN_RESTORATION.add_buff(RESTO_ASCENDANCE)


def remove_buffs_from_casts(
        actor: warcraftlogs_actor.BaseActor,
        cast_spell_ids: set[int],
        buff_spell_ids: set[int],
        proc_spell_id: int,
        tolerance = 500, # ms
    ):
    for cast in actor.casts:
        print(cast, cast.event_type)

    casts = [cast for cast in actor.casts if cast.spell_id in cast_spell_ids and cast.event_type == "cast"]
    buffs = [cast for cast in actor.casts if cast.spell_id in buff_spell_ids and cast.event_type == "applybuff"]

    if not casts and buffs:
        return

    # filter out Buffs triggered by casts
    for buff in buffs:
        closest = min(casts, key=lambda c: abs(c.timestamp - buff.timestamp))
        diff = abs(buff.timestamp - closest.timestamp)
        if diff < tolerance:
            buff.spell_id = -1
        else:
            buff.spell_id = proc_spell_id
    
    actor.casts = [cast for cast in actor.casts if cast.spell_id > 0]


def split_ascendance_procs(actor: warcraftlogs_actor.BaseActor, status: str):
    if status != "success":
        return
    if not actor:
        return
    
    ascendance_casts = {RESTO_ASCENDANCE.spell_id, }
    ascendance_buffs = {RESTO_ASCENDANCE.spell_id, }
    remove_buffs_from_casts(
        actor,
        ascendance_casts,
        ascendance_buffs,
        DRE.spell_id
    )


def clip_ascendance_procs(actor: warcraftlogs_actor.BaseActor, status: str):
    """If someone casts Ascendance before the buff expires, clip it to 6s."""
    for cast in actor.casts:
        if cast.spell_id == DRE.spell_id and cast.duration:
            cast.duration = min(cast.duration, 6000)

warcraftlogs_actor.BaseActor.event_actor_load.connect(split_ascendance_procs)
warcraftlogs_actor.BaseActor.event_actor_load.connect(clip_ascendance_procs)
