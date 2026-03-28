"""Define the Druid Class and all its Specs and Spells."""

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
from lorgs.models.wow_spell import SpellTag, WowSpell


COLOR_INCARNATION = "hsl(230, 60%, 70%)"


################################################################################
# Class
#
DRUID = WowClass(id=11, name="Druid", color="#FF7C0A")

################################################################################
# Specs
#
DRUID_BALANCE     = WowSpec(id=102, role=RDPS, wow_class=DRUID, name="Balance")
DRUID_FERAL       = WowSpec(id=103, role=MDPS, wow_class=DRUID, name="Feral")
DRUID_GUARDIAN    = WowSpec(id=104, role=TANK, wow_class=DRUID, name="Guardian")
DRUID_RESTORATION = WowSpec(id=105, role=HEAL, wow_class=DRUID, name="Restoration")

################################################################################
# Spells
#
DRUID.add_spell(             spell_id=391528, cooldown=60,  duration=4,  color=COL_NF,    name="Convoke the Spirits",            icon="ability_ardenweald_druid.jpg", tags=[SpellTag.RAID_CD])
# DRUID.add_spell(             spell_id=323546, cooldown=180, duration=20, color=COL_VENTR, name="Ravenous Frenzy",                icon="ability_revendreth_druid.jpg",              show=False)


# TODO: find spell ids
# DRUID.add_spell(
#     name="Heart of the Wild",
#     spell_id=??,
#     cooldown=300,
#     duration=45,
#     color="#fcdf03",
#     icon="spell_holy_blessingofagility.jpg",
#     show=False,
#     tags=[SpellTag.TANK]
#     variations=[
# 
#     ]
# )
# 

# Utils
DRUID.add_spell(             spell_id=106898, cooldown=120, duration=8,                   name="Stampeding Roar",                icon="spell_druid_stampedingroar_cat.jpg",        show=False, variations=[77764, 77761], tags=[SpellTag.MOVE])

# Defensives
DRUID.add_spell(             spell_id=22812, cooldown=60, duration=8, name="Barkskin",                icon="spell_nature_stoneclawtotem.jpg",              show=False, tags=[SpellTag.DEFENSIVE])


BEAR_FORM = WowSpell(spell_id=5487, name="Bear Form", icon="ability_racial_bearform.jpg", show=False, event_type="applybuff", tags=[SpellTag.DEFENSIVE])
BEAR_FORM.spell_type = DRUID.name_slug
BEAR_FORM.color = DRUID.color
DRUID_BALANCE.add_buff(BEAR_FORM)
DRUID_FERAL.add_buff(BEAR_FORM)
DRUID_RESTORATION.add_buff(BEAR_FORM)


SURVIVAL_INSTINCTS = WowSpell(spell_id=61336,  cooldown=180, duration=6,                   name="Survival Instincts",             icon="ability_druid_tigersroar.jpg", tags=[SpellTag.DEFENSIVE])
SURVIVAL_INSTINCTS.spell_type = DRUID.name_slug
SURVIVAL_INSTINCTS.color = DRUID.color
DRUID_FERAL.add_spell(SURVIVAL_INSTINCTS)
DRUID_GUARDIAN.add_spell(SURVIVAL_INSTINCTS)


# Offensive
CELESTIAL_ALIGNMENT = DRUID_BALANCE.add_spell(
    spell_id=383410,
    cooldown=120,
    duration=15,
    name="Celestial Alignment",
    color=COLOR_INCARNATION,
    icon="spell_nature_natureguardian.jpg",
    tags=[SpellTag.DAMAGE],
    variations=[
        383410, # CA + Orbital Strike
        194223, # CA + Whirling Stars (2 charges)
        390414, # Incarn + Orbital Strike
        102560, # Incarn + Whirling Stars (2 charges)
    ],
)
DRUID_BALANCE.add_spell(     spell_id=205636, cooldown=60,  duration=10, color="#C7B064", name="Force of Nature",                icon="ability_druid_forceofnature.jpg",           show=False)
DRUID_BALANCE.add_spell(     spell_id=202770, cooldown=60,  duration=8,  color="#749cdb", name="Fury of Elune",                icon="ability_druid_dreamstate.jpg",              show=False)
DRUID_BALANCE.add_spell(     spell_id=1233346, cooldown=32,  duration=15, color="#DAA925", name="Solar Eclipse",                icon="ability_druid_eclipseorange.jpg",  show=False)
DRUID_BALANCE.add_spell(     spell_id=1233272, cooldown=32,  duration=15, color="#4D4BE4", name="Lunar Eclipse",                icon="ability_druid_eclipse.jpg",        show=False)


DRUID_FERAL.add_spell(       spell_id=106951, cooldown=120, duration=15, color=COLOR_INCARNATION, name="Berserk",                        icon="ability_druid_berserk.jpg", variations=[102543], tags=[SpellTag.DAMAGE])
DRUID_FERAL.add_spell(       spell_id=58984,  cooldown=120,              color="#999999", name="Shadowmeld",                     icon="ability_ambush.jpg",                        show=False)
# DRUID_FERAL.add_spell(       spell_id=108291, cooldown=300, duration=45, color="#fcdf03", name="Hearth of the Wild",             icon="spell_holy_blessingofagility.jpg")
# DRUID_FERAL.add_buff(        spell_id=197625,                            color="#11cff5", name="Moonkin Form",                   icon="spell_nature_forceofnature.jpg")
DRUID_FERAL.add_buff(        spell_id=274837, cooldown=45,  duration=6,  color="#c43333", name="Feral Frenzy",                   icon="ability_druid_rake.jpg", show=False)
DRUID_FERAL.add_buff(        spell_id=5217,   cooldown=30,  duration=6,  color="#fcdf03", name="Tiger's Fury",                   icon="ability_mount_jungletiger.jpg", show=False)


DRUID_GUARDIAN.add_spell(    spell_id=61336,  cooldown=180, duration=6,                     name="Survival Instincts",             icon="ability_druid_tigersroar.jpg", tags=[SpellTag.TANK])
DRUID_GUARDIAN.add_spell(    spell_id=102558, cooldown=180, duration=30, color=COLOR_INCARNATION, name="Incarnation: Guardian of Ursoc", icon="spell_druid_incarnation.jpg", variations=[50334], tags=[SpellTag.TANK])
DRUID_GUARDIAN.add_spell(    spell_id=22842,  cooldown=36,  duration=3,                     name="Frenzied Regeneration",          icon="ability_bullrush.jpg",           show=False)
DRUID_GUARDIAN.add_spell(    spell_id=204066, cooldown=60,  duration=8,  color="#52A9C4", name="Lunar Beam",                     icon="spell_nature_moonglow.jpg",           show=False)


DRUID_RESTORATION.add_spell( spell_id=740,    cooldown=150, duration=6,  color="#6cbfd9", name="Tranquility",                    icon="spell_nature_tranquility.jpg", tags=[SpellTag.RAID_CD])
TREE_OF_LIFE = DRUID_RESTORATION.add_spell(spell_id=33891,  cooldown=120, duration=30, color=COLOR_INCARNATION, name="Incarnation: Tree of Life", icon="ability_druid_improvedtreeform.jpg", tags=[SpellTag.RAID_CD])


REFORESTATION = DRUID_RESTORATION.add_buff(
    spell_id=392360,
    cooldown=0,
    duration=9,
    color="#339944",
    name="Reforestation",
    icon="inv_herbalism_70_yserallineseed.jpg",
    show=False,
    event_type="removebuff",  # TOL procs when the buff is removed
)


# Additional Spells (not tracked)
REBIRTH = WowSpell(spell_id=20484, name="Rebirth", icon="spell_nature_reincarnation.jpg")


def remove_tol_recasts(actor: warcraftlogs_actor.BaseActor | None, status: str):
    """Remove tol recasts during extended buff duration."""
    if status != "success":
        return
    if not actor:
        return

    tol_casts = [cast for cast in actor.casts if cast.spell_id == TREE_OF_LIFE.spell_id and cast.event_type == "cast"]
    duration = TREE_OF_LIFE.cooldown * 1000

    prev = None
    for cast in tol_casts:
        if prev:
            diff = cast.timestamp - prev.timestamp
            if diff < duration:
                cast.spell_id = -1
                continue

        prev = cast
    actor.casts = [cast for cast in actor.casts if cast.spell_id > 0]
    
warcraftlogs_actor.BaseActor.event_actor_load.connect(remove_tol_recasts)
