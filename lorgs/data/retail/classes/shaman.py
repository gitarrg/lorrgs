# """Define the Shaman Class its Specs and Spells."""

# pylint: disable=line-too-long
# pylint: disable=bad-whitespace
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# fmt: off

# IMPORT STANDARD LIBRARIES
from typing import override

# IMPORT LOCAL LIBRARIES
from lorgs.data.constants import *
from lorgs.data.retail.roles import HEAL, MDPS, RDPS
from lorgs.models.warcraftlogs_cast import Cast
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_role import WowRole
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag


################################################################################
# Class
#
SHAMAN = WowClass(id=7, name="Shaman", color="#0070DD")

################################################################################
# Specs
#
SHAMAN_ELEMENTAL   = WowSpec(id=262, index=1, role=RDPS, wow_class=SHAMAN, name="Elemental")
SHAMAN_ENHANCEMENT = WowSpec(id=263, index=2, role=MDPS, wow_class=SHAMAN, name="Enhancement")


class RestorationShaman(WowSpec):

    id: int = 264
    index: int = 3
    name: str = "Restoration"
    short_name: str = "Resto"
    role: WowRole = HEAL
    wow_class: WowClass = SHAMAN

    @override
    def process_casts(self, casts: list[Cast]) -> list[Cast]:
        """Report a short Ascendance buff as a Deeply Rooted Elements proc."""
        # Full Ascendance is 15s or more. A proc is about 6s; 13s still counts as a proc
        # so a double proc is not reported as a manual cast.
        proc_duration_ms = 6_000
        proc_max_ms = 13_000
        for cast in casts:
            if cast.spell_id != ASCENDANCE.spell_id or cast.event_type != "applybuff":
                continue
            duration = cast.duration or proc_duration_ms
            cast.duration = duration
            if duration < proc_max_ms:
                cast.spell_id = DEEPLY_ROOTED_ELEMENTS.spell_id
        return casts


SHAMAN_RESTORATION = RestorationShaman()

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
SHAMAN_ENHANCEMENT.add_spell(  spell_id=114051, cooldown=10, duration=15,  color="#ffcb6b", name="Ascendance",                 icon="spell_fire_elementaldevastation.jpg", tags=[SpellTag.DAMAGE])
SHAMAN_ENHANCEMENT.add_spell(  spell_id=197214, cooldown=30,               color="hsl(10 80% 70%)", name="Sundering",          icon="ability_rhyolith_lavapool.jpg", show=False)
SHAMAN_ENHANCEMENT.add_spell(  spell_id=1218090,                           color="hsl(180 60% 60%)", name="Primordial Storm",  icon="ability_shaman_ascendance.jpg", show=False)


SHAMAN_RESTORATION.add_spell(  spell_id=108280, cooldown=180, duration=10,                    name="Healing Tide Totem",         icon="ability_shaman_healingtide.jpg", tags=[SpellTag.RAID_CD])
SHAMAN_RESTORATION.add_spell(  spell_id=98008,  cooldown=180, duration=6,  color="#24b385", name="Spirit Link Totem",          icon="spell_shaman_spiritlink.jpg", tags=[SpellTag.RAID_CD])

# Queried as Ascendance; a short buff is reported as a Deeply Rooted Elements proc.
ASCENDANCE = SHAMAN_RESTORATION.add_buff(   spell_id=114052, cooldown=180,              color="hsl(40 100% 70%)", name="Ascendance",             icon="spell_fire_elementaldevastation.jpg", tags=[SpellTag.RAID_CD])
DEEPLY_ROOTED_ELEMENTS = SHAMAN_RESTORATION.add_buff(   spell_id=378270,                            color="hsl(40 90% 60%)",  name="Deeply Rooted Elements", icon="inv_misc_herb_liferoot_stem.jpg", show=False, query=False)
