"""Belo'ren, Child of Al'ar


>>> PYTHONPATH=. uv run --env-file=.env scripts/load_report.py "https://www.warcraftlogs.com/reports/QCcJTmxyrGdpZNgK?fight=13"

"""

from lorgs.data.classes import *  # noqa: F403
from lorgs.models.raid_boss import RaidBoss


BELOREN = RaidBoss(
    id=3182,
    name="Belo'ren, Child of Al'ar",
    nick="Belo'ren",
    icon="inv_120_raid_marchonqueldanas_lightvoidphoenix.jpg",
)
boss = BELOREN


################################################################################
# Trinkets


################################################################################
# Spells


# AOV + assignments
boss.add_cast(
    spell_id=1242515,
    name="Voidlight Convergence",
    duration=6,
    color="rgb(230, 46, 113)",
    icon="inv_12_dualityphoenix_lightvoid_channel.jpg",
)


# group soak
boss.add_cast(
    spell_id=1241291,
    name="Light Dive",
    duration=8,
    color="rgb(237, 208, 76)",
    icon="inv_phoenix2pet_yellow.jpg",
    variations=[
        1241340,  # Void Dive
    ],
)
# group soak
# boss.add_cast(
#     spell_id=1241340,
#     name="Void Dive",
#     duration=8,
#     color="rgb(100, 62, 201)",
#     icon="inv_phoenix2pet.jpg",
# )


# lines to soak
boss.add_cast(
    spell_id=1242260,
    name="Infused Quills",
    duration=6,
    color="rgb(222, 87, 222)",
    icon="ability_evoker_azurestrike.jpg",
)



# Tank Combo
# - void edict
# - light edict
# - voidlight edict


# Rebirth = intermission cast
boss.add_cast(
    spell_id=1246709,
    name="Death Drop + Rebirth",
    duration=0.5 + 30,  # Death Drop + 30sec Rebirth
    color="rgb(74, 169, 247)",
    icon="inv_12_dualityphoenix_phoenix_rebirth.jpg",
    event_type="begincast",
)




"""
boss.add_cast(
    spell_id=1246709,
    name="Death Drop",
    duration=6,
    color="rgb(74, 169, 247)",
    icon="inv_phoenix2mount_blue.jpg",
    event_type="begincast",
)

boss.add_cast(
    spell_id=1242792,
    name="Incubation of Flames",
    duration=30,
    color="rgb(50, 207, 99)",
    icon="inv_12_dualityphoenix_lightvoid_attack.jpg",
)


boss.add_cast(
    spell_id=1242981,
    name="Radiant Echoes",
    duration=25,
    color="rgb(227, 131, 48)",
    icon="spell_holy_summonlightwell.jpg",
)

boss.add_cast(
    spell_id=1244344,
    name="Eternal Burns",
    duration=8,
    color="rgb(53, 87, 189)",
    icon="spell_frost_manaburn.jpg",
)

boss.add_cast(
    spell_id=1260763,
    name="Guardian's Edict",
    duration=4,
    color="rgb(181, 142, 109)",
    icon="spell_holy_serendipity.jpg",
)
"""


################################################################################
# Phases

boss.add_phase(name="I{phase}", spell_id=1246709, event_type="begincast")  # Death Drop
boss.add_phase(name="P1 ({phase})", spell_id=1241313, event_type="cast") # Rebirth
