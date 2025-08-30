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
    color="rgb(107, 64, 227)",
    icon="ability_mage_arcanebarrage.jpg",
)


# tank: drop big circle far
boss.add_cast(
    spell_id=1219263,
    name="Obliteration Arcanocannon",
    duration=6,
    color="rgb(156, 255, 255)",
    icon="ability_monk_forcesphere_arcane.jpg",
)


# Group Soak
boss.add_cast(
    spell_id=1219531,
    name="Eradicating Salvo",
    duration=5,
    color="rgb(219, 103, 245)",
    icon="spell_arcane_invocation.jpg",
)


# Intermission / P2
boss.add_buff(
    spell_id=1241303,
    name="Protocol: Purge",
    color="rgb(247, 27, 108)",
    icon="spell_arcane_blast.jpg",
    wowhead_data="spell=1220981",  # the channel has a better tooltip
)

# Note: Bart uses different Spell IDs.. but the PTR Log from NS I was testing with was working fine.
# protocol_purge_cast_IDs = ({1220489, 1220553, 1220555},)
# protocol_purge_aura_IDs = ({1220618, 1220981, 1220982},)


################################################################################
# Phases

# ignore the first cast
boss.add_phase(name="P1 ({count})", spell_id=1223364, event_type="cast", count=2)
boss.add_phase(name="P1 ({count})", spell_id=1223364, event_type="cast", count=3)
boss.add_phase(name="P1 ({count})", spell_id=1223364, event_type="cast", count=4)
boss.add_phase(name="P1 ({count})", spell_id=1223364, event_type="cast", count=5)
