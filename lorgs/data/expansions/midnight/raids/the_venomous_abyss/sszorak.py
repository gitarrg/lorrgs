"""Sszorak (The Venomous Abyss).

PTR PopTar
https://www.warcraftlogs.com/reports/X8Vfm3W7gczqGdaJ?fight=23
"""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss


SSZORAK = RaidBoss(
    id=3420,
    name="Sszorak",
    nick="Sszorak",
    icon="inv_121_raid_achievement_brute.jpg",
    # phase_type=RaidBoss.PhaseType.DYNAMIC,
)
boss = SSZORAK


################################################################################
# Trinkets


################################################################################
# Spells


# Frontal Soak
boss.add_cast(
    spell_id=1277027,
    name="Mutilate",
    duration=3,
    color="rgb(112, 86, 240)",
    icon="inv_ability_poison_missile.jpg",
    show=False,
)
# Sszorak rakes his venom-coated claws in a frontal cone,
# inflicting 4792088 Nature damage split evenly among players struck and
# afflicting them with Mutilated Gash.
#
# If Mutilate strikes fewer than 5 players, it inflicts deadly damage.


# Intermission
boss.add_cast(
    spell_id=1286033,
    name="Dig In",
    duration=25,
    color="rgb(181, 60, 13)",
    icon="ability_ghoulfrenzy.jpg",
)
# Channeled (25 sec cast)
# Sszorak hunkers down during Howling Maelstrom, increasing his damage taken by 30% for 25 sec.


# random dot
boss.add_cast(
    spell_id=1305959,
    name="Venomous Surge",
    duration=12,
    color="rgb(136, 227, 79)",
    icon="ability_creature_poison_06.jpg",
)
# Venomous Surge
# Channeled (4 sec cast)
# Sszorak heaves fresh venom onto several players, inflicting 100009 Nature damage every 1 sec for 10 sec.


boss.add_cast(
    spell_id=1285425,
    name="Raging Crosswinds",
    duration=8,
    color="rgb(163, 160, 122)",
    icon="ability_skyreach_wind.jpg",
)
# The Altar of the Six Winds imbues several players with roiling winds,
# inflicting 20835 Nature damage every 1 sec for 8 sec.


"""
boss.add_cast(
    spell_id=1285732,
    name="Howling Maelstrom",
    duration=23.5,
    color="rgb(174, 181, 181)",
    icon="spell_nature_cyclone.jpg",
)


boss.add_cast(
    spell_id=1296898,
    name="Unbound Ferocity",
    duration=30,
    color="rgb(237, 19, 48)",
    icon="spell_shadow_unholyfrenzy.jpg",
)
# Sszorak flies into a killing frenzy, increasing his damage done by 500% and attack speed by 50% until all his foes are left dead or dying.

"""
