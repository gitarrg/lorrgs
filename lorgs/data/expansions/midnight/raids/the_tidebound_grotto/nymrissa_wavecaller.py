"""Nymrissa Wavecaller (The Tidebound Grotto).

<The Early Shift>
PYTHONPATH=. uv run --env-file=.env scripts/load_report.py "https://www.warcraftlogs.com/reports/WjQKfxr4zV9nhmDg?fight=12"

"""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss


NYMRISSA_WAVECALLER = RaidBoss(
    id=3379,
    name="Nymrissa Wavecaller",
    nick="Nymrissa",
    icon="achievement_boss_elitenagamale.jpg",
    phase_type=RaidBoss.PhaseType.DYNAMIC,
)
boss = NYMRISSA_WAVECALLER


################################################################################
# Trinkets


################################################################################
# Spells


# Summon Bubble / Murlocs
boss.add_cast(
    spell_id=1284015,
    name="Alluring Bubble",
    duration=45,  # bubble lifetime until Pop!
    color="rgb(55, 225, 237)",
    icon="inv_elemental_primal_water.jpg",
)
# 5 sec cast
# Nymrissa gathers water from the grotto and forms a massive bubble of swirling liquid.
# The bubble entrances curious murlocs, drawing them in.
# Murlocs that enter become Bubblefin Berserkers.


boss.add_cast(
    spell_id=1258150,
    name="Pop!",
    duration=2,
    color="rgb(227, 18, 91)",
    icon="ability_shawaterelemental_reform.jpg",
)
# The bubble pops, unleashing a surge of pressurized water that inflicts Frost damage
# to all players and knocks them away.


# Raid AOE
boss.add_cast(
    spell_id=1260837,
    name="Abyssal Rain",
    duration=4,
    color="rgb(70, 89, 232)",
    icon="spell_fire_bluerainoffire.jpg",
)
# Nymrissa channels a torrent of water from the crevices above,
# inflicting Frost damage every 1 sec for 4 sec.
# Applies Drenched (Frost DoT every 2 sec).


boss.add_cast(
    spell_id=1258673,
    name="Swirling Whirlpools",
    duration=4,
    color="rgb(180, 199, 212)",
    icon="inv_elemental_primal_air.jpg",
)
# Nymrissa awakens whirlpools within the grotto that surge toward the Alluring Bubble.
# The whirlpools inflict Frost damage to players in their path.


boss.add_cast(
    spell_id=1313393,
    name="Chilling Frost",
    duration=7.5,
    color="rgb(158, 96, 209)",
    icon="spell_fire_blueimmolation.jpg",
)
# Nymrissa chills players, inflicting Frost damage every 1.5 sec and decreasing
# movement speed by 15% for 7.5 sec.
# Each impact leaves behind a Frost Orb at the player's location.


# Tank
boss.add_cast(
    spell_id=1282937,
    name="Iceblade Flurry",
    duration=5,
    color="rgb(189, 160, 142)",
    icon="inv_polearm_2h_draenorchallenge_d_01_02.jpg",
    show=False,
)
# Nymrissa empowers her weapon with ice, slashing her current target
# for Frost damage every 1 sec for 5 sec.


# Tank
boss.add_cast(
    spell_id=1281951,
    name="Water Jet",
    duration=6,
    color="rgb(189, 160, 142)",
    icon="ability_mage_waterjet.jpg",
    show=False,
)
# Nymrissa condenses surrounding water into a high-pressure jet,
# blasting her target for Frost damage every 1 sec and gradually pushing them away.
# Washes away icy patches on the ground.
# Each hit increases damage taken from Water Jet by 20% for 35 sec.
