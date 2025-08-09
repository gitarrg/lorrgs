"""0:


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/B8TZkGKaXQn6rCFA?fight=9"

"""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.wow_trinket import WowTrinket


ARAZ = RaidBoss(
    id=3132,
    name="Forgeweaver Araz",
    nick="Araz",
    icon="inv_112_achievement_raid_engineer.jpg",
)
boss = ARAZ


################################################################################
# Trinkets

ARAZS_RITUAL_FORGE = WowTrinket(
    spell_id=1232802,
    cooldown=120,
    duration=30,
    name="Araz's Ritual Forge",
    icon="inv_112_raidtrinkets_trinkettechnomancer_ritualengine.jpg",
    item=242402,
)
"""30sec Main Statt, decaying

> Use: Recklessly feed a portion of your essence to the forge, granting you 25742 Primary Stat decaying over 30 sec
> at the cost of 15% of your maximum health. (2 Min Cooldown)

"""
ARAZS_RITUAL_FORGE.add_specs(*ALL_SPECS)


################################################################################
# Phase 1


# pillar spawn?
boss.add_cast(
    spell_id=1231720,
    name="Invoke Collector",
    duration=5,
    color="rgb(237, 221, 116)",
    icon="ability_socererking_arcanefortification.jpg",
)


# [Astral Harvest] = Debuff on 3 players -> Drops Add
boss.add_cast(
    spell_id=1228213,
    name="Astral Harvest",
    duration=7,
    color="rgb(102, 242, 242)",
    icon="ability_warlock_soulswap.jpg",
)


# "[Arcane Obliteration]" = group soak
# -> spawns "Arcana Echo"-Add
boss.add_cast(
    spell_id=1228216,
    name="Astral Harvest",
    duration=7,
    color="rgb(235, 75, 235)",
    icon="spell_arcane_arcanetorrent.jpg",
)

# Silencing Tempest --> not relevant?


boss.add_cast(
    spell_id=1228502,
    name="Overwhelming Power",
    duration=1.2,
    cooldown=46,
    color="rgb(199, 263, 115)",
    icon="ability_mage_netherwindpresence.jpg",
    show=False,
)


################################################################################
# Intermisions

# knockback
boss.add_cast(
    spell_id=1227631,
    name="Arcane Expulsion",
    duration=5,
    color="rgb(232, 28, 92)",
    icon="ability_mage_tormentoftheweak.jpg",
)


boss.add_cast(
    spell_id=1233415,
    name="Mana Splinter",
    duration=12,
    color="rgb(40, 233, 81)",
    icon="inv_112_arcane_debuff.jpg",
)


################################################################################
# Phase 2

boss.add_cast(
    spell_id=1243887,
    name="Void Harvest",
    duration=7,
    color="rgb(102, 242, 242)",
    icon="inv_cosmicvoid_debuff.jpg",
)

boss.add_cast(
    spell_id=1232221,
    name="Death Throes",
    duration=3.5,
    color="rgb(157, 66, 237)",
    icon="inv_112_etherealwraps_empowered_original.jpg",
)


################################################################################
# Phases

boss.add_phase(name="P1 ({count})", spell_id=1230529, event_type="cast")  # Mana Sacrifice
boss.add_phase(name="P2", spell_id=1233076, event_type="applybuff")  # Dark Singularity
