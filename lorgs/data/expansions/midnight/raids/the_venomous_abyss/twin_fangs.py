"""The Twin Fangs (The Venomous Abyss).

The Twin Fangs is a two-target fight that repeats mechanics until defeated.
In this fight, the Twin Fangs build  Eternal Venom within players with their
various abilities and spells. If a player reaches nine stacks of Eternal Venom,
they are instantly killed.  Ravenous Feast, a large group soak, can remove up to
three stacks of Eternal Venom. Watch your stacks and make sure you're soaking when needed!

https://www.warcraftlogs.com/reports/X8Vfm3W7gczqGdaJ?fight=43

"""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss


TWIN_FANGS = RaidBoss(
    id=3421,
    name="The Twin Fangs",
    nick="Twin Fangs",
    icon="ability_rogue_deviouspoisons.jpg",
)
boss = TWIN_FANGS


################################################################################
# Trinkets


################################################################################
# Spells


################################
# Vexhul
boss.add_cast(
    spell_id=1294293,
    name="Vile Flood",
    duration=4,
    cooldown=14,
    color="rgb(20, 227, 55)",
    icon="ICON_PLACEHOLDER.jpg",
)
# Vexhul channels a continuous torrent of toxin in a frontal direction for 14 sec,
# inflicting 416703 Nature damage every 0.5 sec and applying Eternal Venom to players struck.


# add summon
boss.add_cast(
    spell_id=1291404,
    name="Venomous Emergence",
    duration=3,
    color="rgb(102, 212, 135)",
    icon="spell_nature_poisoncleansingtotem.jpg",
)
# Vexhul calls her progeny from the churning sea, inflicting 125011 Nature damage
# and applying Eternal Venom to all players.


# AOE
boss.add_cast(
    spell_id=1290956,
    name="Stir the Depths",
    duration=6,
    color="rgb(161, 184, 61)",
    icon="inv_ability_poison_wave.jpg",
)
# Vexhul thrashes and churns the surrounding sea of venom for 6 sec,
# inflicting 166681 Nature damage to all players every 2 sec and forming waves.
#
# The waves travel across the platform, inflicting 125011 Nature damage every
# 1 sec and applying Eternal Venom to players struck.


# dodge balls?
boss.add_cast(
    spell_id=1289192,
    name="Caustic Deluge",
    duration=5,
    color="rgb(160, 173, 132)",
    icon="inv_ability_poison_beam.jpg",
    show=False,
)

################################
# Ithraz

# Group Soak?
boss.add_cast(
    spell_id=1288538,
    name="Stone Breaker",
    duration=1.5,
    color="rgb(161, 129, 106)",
    icon="ability_smash.jpg",
    show=True,
)
# Ithraz roars, pushing players away. He then slams the platform repeatedly.
# Each impact inflicts 2500220 Physical damage to players within 3.5 yards and
# increases their damage taken from Stone Breaker by 33% for 1.5 min.
# This effect stacks.
#
# If no players are struck, Ithraz instead inflicts 916747 Physical damage to
# all players and knocks them away. This effect ignores armor.


# Summon Adds
boss.add_cast(
    spell_id=1308356,
    name="Rouse the Brood",
    duration=3,
    color="rgb(84, 59, 48)",
    icon="inv_giantsnake_black.jpg",
)
# 3 sec cast
# Ithraz thrashes, calling several Broodlings of Ithraz to the surface and
# releasing a nova of blood that inflicts 208352 Shadow damage to all players.


# Intermission?
boss.add_cast(
    spell_id=1306872,
    name="Sanguine Storm",
    duration=18,
    color="rgb(230, 21, 49)",
    icon="inv_artifact_bloodoftheassassinated.jpg",
)


# Group Soak
boss.add_cast(
    spell_id=1290516,
    name="Ravenous Feast",
    duration=4,
    color="rgb(222, 66, 31)",
    icon="ability_warrior_bloodnova.jpg",
)
# Ithraz attempts to consume players 3 times in quick succession.
# Each strike inflicts 4625407 Physical damage split evenly among players within 14 yards.
# Ithraz consumes 1 application of Eternal Venom from players struck,
# applies Feasted to them, and knocks them away.


boss.add_cast(
    spell_id=1290814,
    name="Coiling Ichor",
    duration=12,
    color="rgb(230, 37, 117)",
    icon="ability_ironmaidens_whirlofblood.jpg",
    show=False,
)


# Tank
boss.add_cast(
    spell_id=1303230,
    name="Blood Torrent",
    duration=5,
    color="rgb(199, 119, 170)",
    icon="inv_artifact_corruptedbloodofzakajz.jpg",
    show=False,
)
