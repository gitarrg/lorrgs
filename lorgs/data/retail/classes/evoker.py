"""Define the Evoker Class and all its Specs and Spells."""

# pylint: disable=line-too-long
# pylint: disable=bad-whitespace
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# fmt: off

# IMPORT STANDARD LIBRARIES
from typing import override

# IMPORT LOCAL LIBRARIES
from lorgs.data.constants import *
from lorgs.data.retail.roles import *
from lorgs.models.warcraftlogs_cast import Cast
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_role import WowRole
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag


COLOR_BRONZE = "#e8bf46"
COLOR_BLACK = "#915f59"
COLOR_RED = "#eb3f3f"


################################################################################
# Class
#
EVOKER = WowClass(id=13, name="Evoker", color="#33937F")

################################################################################
# Specs
#
EVOKER_DEVASTATION  = WowSpec(id=1467, index=1, role=RDPS, wow_class=EVOKER, name="Devastation")


class PreservationEvoker(WowSpec):

    id: int = 1468
    index: int = 2
    name: str = "Preservation"
    role: WowRole = HEAL
    wow_class: WowClass = EVOKER

    @override
    def process_casts(self, casts: list[Cast]) -> list[Cast]:
        """Give Stasis charges their real duration, then drop spells Stasis released."""
        casts = self._calculate_stasis_duration(casts)
        casts = self._filter_stasis_release_spells(casts)
        return casts

    def _calculate_stasis_duration(self, casts: list[Cast]) -> list[Cast]:  # ruff: ignore[no-self-use]
        """Charge then release sets the charge duration. A lone release was charged for the full duration before the pull."""
        charge: Cast | None = None
        prepull: list[Cast] = []
        full_duration_ms = int(STASIS_STORE.duration * 1000)

        for cast in casts:

            # new store
            if cast.spell_id == STASIS_STORE.spell_id:
                charge = cast
                continue

            # new release
            if cast.spell_id == STASIS_RELEASE.spell_id:

                if charge:
                    charge.duration = cast.timestamp - charge.timestamp
                else:
                    prepull.append(Cast(
                        spell_id=STASIS_STORE.spell_id,
                        timestamp=cast.timestamp - full_duration_ms,
                        duration=full_duration_ms,
                    ))

        # no need to sort, prepull is first
        return [*prepull,*casts]

    def _filter_stasis_release_spells(self, casts: list[Cast]) -> list[Cast]:  # ruff: ignore[no-self-use]
        """Drop a stored spell cast within a second of Stasis Pop."""
        release_window_ms = 1_000

        stasis_storable_spells = {
            DREAM_BREATH.spell_id,  # the only spell that we track
        }

        stasis_release: int = -1000

        stasis_casts: list[Cast] = []
        # spells that have been released from Stasis

        for cast in casts:

            if cast.spell_id == STASIS_RELEASE.spell_id:
                stasis_release = cast.timestamp + (cast.duration or int(STASIS_RELEASE.duration * 1000))

            can_be_stored = cast.spell_id in stasis_storable_spells
            within_release_window = cast.timestamp - stasis_release < release_window_ms

            if can_be_stored and within_release_window:
                stasis_casts.append(cast)

        return [cast for cast in casts if cast not in stasis_casts]


EVOKER_PRESERVATION = PreservationEvoker()
EVOKER_AUGMENTATION = WowSpec(id=1473, index=3, role=RDPS, wow_class=EVOKER, name="Augmentation")


################################################################################
# Spells
#

# Defensives
EVOKER.add_spell(spell_id=363916, name="Obsidian Scales",    cooldown=150, duration=12, color=COLOR_BLACK,  icon="inv_artifact_dragonscales.jpg", tags=[SpellTag.DEFENSIVE], show=False)
EVOKER.add_spell(spell_id=370553, name="Tip the Scales",     cooldown=120,              color=COLOR_BRONZE, icon="ability_evoker_tipthescales.jpg", show=False)
EVOKER.add_spell(spell_id=374227, name="Zephyr",             cooldown=120, duration=8,  color="#d6b969",    icon="ability_evoker_hoverblack.jpg", tags=[SpellTag.RAID_CD], show=False)
EVOKER.add_spell(spell_id=374968, name="Time Spiral",        cooldown=120, duration=10, color="#c4d669",    icon="ability_evoker_timespiral.jpg", tags=[SpellTag.RAID_CD, SpellTag.MOVE], show=False)
EVOKER.add_spell(spell_id=406732, name="Spatial Paradox",    cooldown=120, duration=10,                    icon="ability_evoker_stretchtime.jpg", show=False, tags=[SpellTag.MOVE])
EVOKER.add_spell(spell_id=370665, name="Rescue",             cooldown=60,               color="#8bc1ff",  icon="ability_evoker_flywithme.jpg", show=False, tags=[SpellTag.MOVE])


# DPS
EVOKER_DEVASTATION.add_spell(spell_id=368847, name="Firestorm",  cooldown=20,  duration=12, color=COLOR_RED, icon="ability_evoker_firestorm.jpg", tags=[SpellTag.DAMAGE])
EVOKER_DEVASTATION.add_spell(spell_id=375087, name="Dragonrage", cooldown=120, duration=14, color=COLOR_RED, icon="ability_evoker_dragonrage.jpg", tags=[SpellTag.DAMAGE])
EVOKER_DEVASTATION.add_spell(spell_id=433874, name="Deep Breath", cooldown=120,             color=COLOR_BRONZE, icon="ability_evoker_deepbreath.jpg", tags=[SpellTag.DAMAGE])


_filter_tip_the_scales = "IN RANGE FROM type = 'applybuff' AND ability.name = 'Tip the Scales' TO type = 'removebuff' AND ability.name = 'Tip the Scales' END"
tooltip_tip_the_scales_buffed = "Tip the Scales buffed."
EVOKER_DEVASTATION.add_spell(spell_id=382266, name="Fire Breath", cooldown=30, color=COLOR_RED, icon="ability_evoker_firebreath.jpg", extra_filter=_filter_tip_the_scales, tooltip=tooltip_tip_the_scales_buffed)
EVOKER_DEVASTATION.add_spell(spell_id=382411, name="Eternity Surge", cooldown=30, color="#308fbf", icon="ability_evoker_eternitysurge.jpg", extra_filter=_filter_tip_the_scales, tooltip=tooltip_tip_the_scales_buffed)


# HEAL
EVOKER_PRESERVATION.add_spell(spell_id=370960, name="Emerald Communion",  cooldown=180, duration=5,                      icon="ability_evoker_green_01.jpg", tags=[SpellTag.RAID_CD])
EVOKER_PRESERVATION.add_spell(spell_id=363534, name="Rewind",             cooldown=180,              color=COLOR_BRONZE, icon="ability_evoker_rewind.jpg", tags=[SpellTag.RAID_CD])
EVOKER_PRESERVATION.add_spell(spell_id=359816, name="Dreamflight",        cooldown=120, duration=15, color="#33a36d",    icon="ability_evoker_dreamflight.jpg", tags=[SpellTag.RAID_CD])
DREAM_BREATH = EVOKER_PRESERVATION.add_spell(spell_id=355936, name="Dream Breath",       cooldown=30,               color="#59ebb3",  icon="ability_evoker_dreambreath.jpg", show=False)
STASIS_STORE = EVOKER_PRESERVATION.add_spell(spell_id=370537, name="Stasis", cooldown=90, duration=30, color=COLOR_BRONZE, icon="ability_evoker_stasis.jpg", tags=[SpellTag.RAID_CD])
STASIS_RELEASE = EVOKER_PRESERVATION.add_spell(spell_id=370564, name="Stasis Pop", icon=STASIS_STORE.icon, show=False)

# Augmentation
EVOKER_AUGMENTATION.add_buff( spell_id=395296, name="Ebon Might Buff",                            color="#bf8330", icon="spell_sarkareth.jpg", show=False)
EVOKER_AUGMENTATION.add_spell(spell_id=403631, name="Breath of Eons",  cooldown=120, duration=12, color="#e4e267", icon="ability_evoker_breathofeons.jpg", tags=[SpellTag.DAMAGE], variations=[442204])
EVOKER_AUGMENTATION.add_spell(spell_id=404977, name="Time Skip",       cooldown=180,              color="#e8bf46", icon="ability_evoker_timeskip.jpg")
