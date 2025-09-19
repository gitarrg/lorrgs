"""03: The Soul Hunters


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/B8TZkGKaXQn6rCFA?fight=16"

"""

from lorgs.models.raid_boss import RaidBoss
from lorgs.data.classes import *


SOUL_HUNTERS = RaidBoss(
    id=3122,
    name="The Soul Hunters",
    nick="Soul Hunters",
    icon="inv_112_achievement_raid_dhcouncil.jpg",
)
boss = SOUL_HUNTERS


################################################################################
# Spells


boss.add_cast(
    spell_id=1242259,
    name="Spirit Bomb",
    duration=8,
    color="rgb(95, 9, 153)",
    icon="inv_icon_shadowcouncilorb_purple.jpg",
)

boss.add_cast(
    spell_id=1227355,
    name="Voidstep",
    duration=2.5,
    color="rgb(71, 53, 232)",
    icon="inv_netherportal.jpg",
)

boss.add_cast(
    spell_id=1227809,
    name="The Hunt",
    duration=6,
    color="rgb(232, 23, 72)",
    icon="inv_ability_demonhunter_thehunt.jpg",
    extra_filter="source.class = 'Boss'",
)

boss.add_cast(
    spell_id=1240891,
    name="Sigil of Chains",
    duration=2.5,
    color="rgb(252, 242, 38)",
    icon="ability_demonhunter_sigilofchains.jpg",
    show=False,
)

boss.add_cast(
    spell_id=1222232,
    name="Devourer's Ire",
    duration=13,
    color="rgb(240, 53, 125)",
    icon="spell_nzinsanity_shortsighted.jpg",
)


# Tank:

boss.add_cast(
    spell_id=1241833,
    name="Fracture",
    duration=8,
    color="rgb(95, 9, 153)",
    icon="ability_creature_felsunder.jpg",
    show=False,
)


boss.add_cast(
    spell_id=1218103,
    name="Eye Beam",
    duration=4,
    color="rgb(190, 70, 227)",
    icon="ability_demonhunter_eyebeam.jpg",
    show=False,
)


# Intermisisons:

boss.add_cast(
    spell_id=1233093,
    name="Collapsing Star",
    duration=25,
    color="rgb(41, 244, 255)",
    icon="inv_cosmicvoid_nova.jpg",
)

boss.add_cast(
    spell_id=1233863,
    name="Fel Rush",
    duration=24,
    color="rgb(43, 217, 165)",
    icon="ability_demonhunter_felrush.jpg",
)

boss.add_cast(
    spell_id=1227117,
    name="Fel Devastation",
    duration=4.5,
    color="rgb(47, 150, 64)",
    icon="ability_demonhunter_feldevastation.jpg",
)


################################################################################
# Phases

# there are always 2 applications per phase.
# but tbh, the boss timers are static anyways.. so we could remove this
boss.add_phase(name="P1", spell_id=1245978, event_type="applybuff", count=1)  # Soul Tether
boss.add_phase(name="P2", spell_id=1245978, event_type="applybuff", count=3)  # Soul Tether
boss.add_phase(name="P3", spell_id=1245978, event_type="applybuff", count=5)  # Soul Tether
