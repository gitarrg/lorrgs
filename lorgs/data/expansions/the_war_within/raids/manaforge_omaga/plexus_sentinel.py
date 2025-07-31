"""01: Plexus Sentinel


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/AvbNVBmyrKPDCT4L?fight=5"

"""

from lorgs.models.raid_boss import RaidBoss
from lorgs.data.classes import *


PLEXUS_SENTINEL = RaidBoss(
    id=3129,
    name="Plexus Sentinel",
    nick="Plexus Sentinel",
    icon="inv_112_achievement_raid_automaton.jpg",
)
boss = PLEXUS_SENTINEL


################################################################################
# Spells


# drop circles
boss.add_cast(
    spell_id=1219450,
    name="Manifest Matrices",
    duration=6,
    # cooldown=45,
    color="hsl(30, 60%, 50%)",
    icon="ability_mage_arcanebarrage.jpg",
)


# tank: drop big circle far
boss.add_cast(
    spell_id=1219263,
    name="Obliteration Arcanocannon",
    duration=6,
    # cooldown=45,
    # color="hsl(30, 60%, 50%)",
    icon="ability_monk_forcesphere_arcane.jpg",
)


# Group Soak
boss.add_cast(
    spell_id=1219531,
    name="Eradicating Salvo",
    duration=5,
    # cooldown=45,
    # color="hsl(30, 60%, 50%)",
    icon="spell_arcane_invocation.jpg",
)


# Intermission / P2
boss.add_buff(
    spell_id=1241303,
    name="Protocol: Purge",
    # duration=6,
    # cooldown=45,
    # color="hsl(30, 60%, 50%)",
    icon="spell_arcane_blast.jpg",
    wowhead_data="spell=1220981",  # the channel has a better tooltip
)
