"""Lightblinded Vanguard


>>> PYTHONPATH=. uv run --env-file=.env scripts/load_report.py "https://www.warcraftlogs.com/reports/QCcJTmxyrGdpZNgK?fight=32"


"""

from lorgs.data.classes import *  # noqa: F403
from lorgs.models.raid_boss import RaidBoss


LIGHTBLINDED_VANGUARD = RaidBoss(
    id=3180,
    name="Lightblinded Vanguard",
    nick="Vanguard",
    icon="inv_120_raid_voidspire_paladintrio.jpg",
)
boss = LIGHTBLINDED_VANGUARD


################################################################################
# Trinkets

# [Litany of Lightblind Wrath]


################################################################################
# Spells



#################################
# Lightblood


# Ultimate
# boss dmg buff inside circle + soak circle
boss.add_cast(
    spell_id=1248449,
    name="Aura of Wrath",
    duration=15,
    color="rgb(237, 198, 40)",
    icon="spell_holy_sealofwrath.jpg",
)

# group soaks
boss.add_cast(
    spell_id=1248994,
    name="Execution Sentence",
    duration=10,
    color="rgb(204, 182, 94)",
    icon="spell_paladin_executionsentence.jpg",
)


#################################
# Bellamy

# boss dmg reduction inside circle
boss.add_buff(
    spell_id=1246165,
    name="Aura of Devotion",
    color="rgb(36, 67, 242)",
    icon="spell_holy_devotionaura.jpg",
    extra_filter="target.id=240431",  # track only on Bellamy
    #
)


# spread circles
boss.add_cast(
    spell_id=1248644,
    name="Divine Toll",
    duration=20,
    color="rgb(82, 103, 217)",
    icon="inv_ability_paladin_divinetoll.jpg",
    show=False,
)





#################################
# Senn:

# Ulti
boss.add_cast(
    spell_id=1248451,
    name="Aura of Peace",
    duration=25,
    color="rgb(228, 59, 237)",
    icon="spell_holy_silence.jpg",
)

# heal absorbs
boss.add_cast(
    spell_id=1248710,
    name="Tyr's Wrath",
    duration=20,
    color="rgb(203, 126, 207)",
    icon="inv_ability_holyfire_debuff.jpg",
)



# heal absorbs
boss.add_buff(
    spell_id=1248674,
    name="Sacred Shield",
    color="rgb(186, 139, 114)",
    icon="ability_paladin_blessedmending.jpg",
)


# boss.add_cast(
#     spell_id=1249130,
#     name="Trampling Charge",
#     duration=3,
#     color="rgb(186, 139, 114)",
#     icon="inv_lightforgedelekk.jpg",
# )

boss.add_cast(
    spell_id=1255738,
    name="Searing Radiance",
    duration=15,
    color="rgb(106, 50, 209)",
    icon="inv_ability_holyfire_buff.jpg",
)


# circles around random players --> spread
boss.add_cast(
    spell_id=1246487,
    name="Avenger's Shield",
    duration=6,
    color="rgb(242, 164, 46)",
    icon="spell_holy_avengersshield.jpg",
    show=False,
)



# Tank Hits
boss.add_cast(
    spell_id=1251857,
    name="Judgment",
    duration=3,
    color="rgb(182, 198, 214)",
    icon="ability_paladin_judgementblue.jpg",
    show=False,
)
boss.add_cast(
    spell_id=1246736,
    name="Judgment",
    duration=3,
    color="rgb(204, 112, 102)",
    icon="ability_paladin_judgementred.jpg",
    show=False,
)

################################################################################
# Phases
