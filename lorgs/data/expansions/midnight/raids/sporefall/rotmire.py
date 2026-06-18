"""Rotmire.

>>> PYTHONPATH=. uv run --env-file=.env scripts/load_report.py "https://www.warcraftlogs.com/reports/ybNtPVgaDWqQYfLh?fight=37"

"""

from lorgs.data.classes import *  # noqa: F403
from lorgs.models.raid_boss import RaidBoss


ROTMIRE = RaidBoss(
    id=3159,
    name="Rotmire",
    nick="Rotmire",
    icon="inv_1207_achievement_raid_fungariangiant_fungalgiant.jpg",
)
boss = ROTMIRE


################################################################################
# Trinkets


################################################################################
# Spells


boss.add_cast(
    spell_id=1221637,
    name="Fungal Bloom",
    duration=16,
    color="rgb(219, 81, 237)",
    icon="inv_misc_herb_plaguebloom.jpg",
)


boss.add_cast(
    spell_id=1221622,
    name="Awaken Fungi",
    duration=8,
    color="rgb(227, 111, 175)",
    icon="inv_misc_food_96_zangarcaps.jpg",
)


boss.add_cast(
    spell_id=1222088,
    name="Festering Vines",
    duration=8,
    color="rgb(27, 128, 87)",
    icon="ability_creature_poison_04.jpg",
)


boss.add_cast(
    spell_id=1221787,
    name="Bursting Postules",
    duration=2,
    color="rgb(153, 52, 97)",
    icon="inv_misc_herb_zoanthid.jpg",
)


boss.add_cast(
    spell_id=1221781,
    name="Putrid Fist",
    duration=2,
    color="rgb(179, 176, 145)",
    icon="inv_misc_herb_ancientlichen.jpg",
    show=False,
)
