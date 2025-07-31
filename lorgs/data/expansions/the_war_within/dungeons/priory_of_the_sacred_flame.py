# IMPORT LOCAL LIBRARIES
from lorgs.data.classes import *
from lorgs.models.dungeon import Dungeon
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Trinkets

BURSTING_LIGHTSHARD = WowTrinket(
    spell_id=443536,
    cooldown=120,
    name="Bursting Lightshard",
    icon="inv_arathordungeon_fragment_color4.jpg",
    item=219310,
)
"""On-Use placed pet, pulses for Damage

> Use: Summon a Bursting Lightspawn which sacrifices its health to unleash Bursts of Light,
> inflicting 47520 Holy damage split between nearby enemies every 2 sec while it lives. (2 Min Cooldown)
"""

SIGNET_OF_THE_PRIORY = WowTrinket(
    spell_id=443531,
    cooldown=120,
    duration=20,
    name="Signet of the Priory",
    icon="inv_arathordungeon_signet_color1.jpg",
    item=219308,
)
"""On-Use secondary stat + party buff

> Use: Raise your signet to the Light, increasing your highest secondary stat by 2756 for 20 sec.
> Your act inspires nearby signetbearers within your party, granting them 73 of the same stat for 20 sec. (2 Min Cooldown)
"""
SIGNET_OF_THE_PRIORY.add_specs(*ALL_SPECS)


TOME_OF_LIGHTS_DEVOTION = "[Tome of Light's Devotion]"
"""Absorb and some one use. (Tank Only)

spell_id=443535
https://www.wowhead.com/item=219309/tome-of-lights-devotion

> Equip: Advance to the 50 Verses of Inner Resilience, reading as you are attacked.
> Inner Resilience increases your armor by 97 and grants your attacks a chance to
> invoke a ward which absorbs 3781 Magic damage. When finished, sift through the passages to another chapter.

> Valid only for tank specializations. (750ms cooldown)
> Use: Sift through the passages in the tome with increased Radiance. (1 Min, 30 Sec Cooldown)
"""


################################################################################

PRIORY_OF_THE_SACRED_FLAME = Dungeon(
    name="Priory of the Sacred Flame",
    trinkets=[
        SIGNET_OF_THE_PRIORY,
    ],
)
