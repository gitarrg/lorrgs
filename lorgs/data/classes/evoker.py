"""Define the Evoker Class and all its Specs and Spells."""

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
EVOKER_DEVASTATION = WowSpec(role=RDPS, wow_class=EVOKER, name="Devastation")
EVOKER_PRESERVATION = WowSpec(role=HEAL, wow_class=EVOKER, name="Preservation")
EVOKER_AUGMENTATION = WowSpec(role=RDPS, wow_class=EVOKER, name="Augmentation")


################################################################################
# Spells
#

# Defensives
EVOKER.add_spell(spell_id=363916, name="Obsidian Scales",    cooldown=150, duration=12, color=COLOR_BLACK,  icon="inv_artifact_dragonscales.jpg", tags=[SpellTag.DEFENSIVE], show=False)
EVOKER.add_spell(spell_id=374348, name="Renewing Blaze",     cooldown=150, duration=8,  color=COLOR_RED,    icon="ability_evoker_masterylifebinder_red.jpg", tags=[SpellTag.DEFENSIVE], show=False)
EVOKER.add_spell(spell_id=370553, name="Tip the Scales",     cooldown=120,              color=COLOR_BRONZE, icon="ability_evoker_tipthescales.jpg", show=False)
EVOKER.add_spell(spell_id=374227, name="Zephyr",             cooldown=120, duration=8,  color="#d6b969",    icon="ability_evoker_hoverblack.jpg", tags=[SpellTag.RAID_CD], show=False)
EVOKER.add_spell(spell_id=374968, name="Time Spiral",        cooldown=120, duration=10, color="#c4d669",    icon="ability_evoker_timespiral.jpg", tags=[SpellTag.RAID_CD, SpellTag.MOVE], show=False)
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
EVOKER_PRESERVATION.add_spell(spell_id=443328, name="Engulf",             cooldown=30,               color="#dd405a",  icon="inv_ability_flameshaperevoker_engulf.jpg", show=False)
EVOKER_PRESERVATION.add_spell(spell_id=355936, name="Dream Breath",       cooldown=30,               color="#59ebb3",  icon="ability_evoker_dreambreath.jpg", show=False)
STASIS_CHARGE = EVOKER_PRESERVATION.add_spell(spell_id=370537, name="Stasis", cooldown=90, color=COLOR_BRONZE, icon="ability_evoker_stasis.jpg", tags=[SpellTag.RAID_CD])
STASIS_RELEASE = EVOKER_PRESERVATION.add_spell(spell_id=370564, name="Stasis Pop", icon=STASIS_CHARGE.icon, show=False)

# Augmentation
EVOKER_AUGMENTATION.add_buff( spell_id=395296, name="Ebon Might Buff",                            color="#bf8330", icon="spell_sarkareth.jpg", show=False)
EVOKER_AUGMENTATION.add_spell(spell_id=403631, name="Breath of Eons",  cooldown=120, duration=12, color="#e4e267", icon="ability_evoker_breathofeons.jpg", tags=[SpellTag.DAMAGE], variations=[442204])
EVOKER_AUGMENTATION.add_spell(spell_id=404977, name="Time Skip",       cooldown=180,              color="#e8bf46", icon="ability_evoker_timeskip.jpg")
EVOKER_AUGMENTATION.add_spell(spell_id=406732, name="Spatial Paradox", cooldown=120, duration=10,                    icon="ability_evoker_stretchtime.jpg", show=False, tags=[SpellTag.MOVE])



def calculate_stasis_duration(actor: warcraftlogs_actor.BaseActor, status: str) -> None:
    """Calculates the duration between charging and releasing the stasis."""
    if status != "success":
        return
    if not actor:
        return


    charge_event = None

    for cast in actor.casts:

        if cast.spell == STASIS_CHARGE:
            charge_event = cast
            continue

        if cast.spell == STASIS_RELEASE:

            if charge_event:
                charge_event.duration = cast.timestamp - charge_event.timestamp

                # keep the release spell for MRT purposes
                ## cast.spell_id = -1  # we no longer need this.

            else: # stasis was charged pre pull
                cast.spell_id = STASIS_CHARGE.spell_id
                cast.duration = cast.timestamp # create a charge event at 0:00
                cast.timestamp = 0


    actor.casts = [cast for cast in actor.casts if cast.spell_id > 0]


warcraftlogs_actor.BaseActor.event_actor_load.connect(calculate_stasis_duration)


# list[int]: Spells that are able to be stores in Stasis
STATIS_SPELLS = [
    443328, # Engulf
    355936, # Dream Breath
]


def filter_stasis_spells(actor: warcraftlogs_actor.BaseActor, status: str) -> None:
    """Remove Spells cast by stasis.
    
    Those are no manual casts, and thus can be confusing if they show up in the timeline

    """
    if status != "success":
        return
    if not actor:
        return
    
    last_stasis_end = -99999
    threashold = 1000  # 1sec. I takes around 1sec for Stasis to release.

    for cast in actor.casts:

        # Update Stasis Release Time
        if cast.spell_id == 370562:
            last_stasis_end = cast.timestamp + cast.get_duration()
            continue

        # Filter out Spells within 1sec of Stasis Release,
        # assuming they arn't real casts
        in_stasis_threashold = (cast.timestamp - last_stasis_end) < threashold
        statis_spell_id = cast.spell_id in STATIS_SPELLS
        if in_stasis_threashold and statis_spell_id:
            cast.spell_id = -1

    actor.casts = [cast for cast in actor.casts if cast.spell_id > 0]


warcraftlogs_actor.BaseActor.event_actor_load.connect(filter_stasis_spells)
