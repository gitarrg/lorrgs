"""Chimaerus


# mythic ptr kill
>>> PYTHONPATH=. uv run --env-file=.env scripts/load_report.py "https://www.warcraftlogs.com/reports/8dKxaHfhgrpTL4q2?fight=10"

# heroic PTR 7:03 wipe
>>> PYTHONPATH=. uv run --env-file=.env scripts/load_report.py "https://www.warcraftlogs.com/reports/xK7dgA6yVDharLpJ?fight=4"


"""

from lorgs.data.classes import *  # noqa: F403
from lorgs.models.raid_boss import RaidBoss


CHIMAERUS = RaidBoss(
    id=3306,
    name="Chimaerus",
    nick="Chimaerus",
    icon="inv_120_raid_dreamwell_malformedmanifestation.jpg",
)
boss = CHIMAERUS


################################################################################
# Trinkets


################################################################################
# Spells


# tank soak --> soak to get into other phase
boss.add_cast(
    spell_id=1262289,
    name="Alndust Upheaval",
    duration=5,
    color="rgb(164, 235, 229)",
    icon="ability_earthen_azeritesurge.jpg",
)


# spawn adds
boss.add_cast(
    spell_id=1258610,
    name="Rift Emergence",
    duration=3,
    color="rgb(64, 95, 219)",
    icon="inv_azeritefireball.jpg",
)


# vacuum cleaner debuff
boss.add_cast(
    spell_id=1257087,
    name="Consuming Miasma",
    duration=8,
    color="rgb(50, 150, 255)",
    icon="spell_azerite_essence_16.jpg",
    show=False,
)


# big aoe
boss.add_cast(
    spell_id=1246653,
    name="Caustic Phlegm",
    duration=12,
    color="rgb(168, 204, 75)",
    icon="inv_ability_poison_orb.jpg",
)



######################
#  Phase 2


# consume all adds --> start intermission
boss.add_cast(
    spell_id=1245396,
    name="Consume",
    duration=10,
    color="rgb(242, 19, 64)",
    icon="spell_deathknight_gnaw_ghoul.jpg",
)

# intermission end: knockback + consume adds
boss.add_cast(
    spell_id=1245404,
    name="Ravenous Dive",
    duration=3.5,
    color="rgb(196, 148, 71)",
    icon="ability_earthen_pillar.jpg",
)


"""

boss.add_buff(
    spell_id=1252863,
    name="Insatiable",
    color="rgb(128, 128, 128)",
    icon="spell_shadow_lifedrain.jpg",
    show=False,
)

boss.add_cast(
    spell_id=1246132,
    name="Rift Shroud",
    duration=80,
    color="rgb(157, 242, 104)",
    icon="spell_nature_elementalshields.jpg",
)

boss.add_cast(
    spell_id=1272726,
    name="Rending Tear",
    duration=3.5,
    color="rgb(240, 71, 41)",
    icon="spell_druid_bloodythrash.jpg",
)

boss.add_cast(
    spell_id=1245452,
    name="Corrupted Devastation",
    duration=5,
    color="rgb(255, 211, 33)",
    icon="spell_azerite_essence02.jpg",
)

boss.add_cast(
    spell_id=1264756,
    name="Rift Madness",
    duration=5,
    color="rgb(242, 41, 242)",
    icon="sha_spell_warlock_demonsoul.jpg",
)
"""

################################################################################
# Phases

boss.add_phase(name="I{count}", spell_id=1245396, event_type="cast")
boss.add_phase(name="P{phase}", spell_id=1245404, event_type="cast")
