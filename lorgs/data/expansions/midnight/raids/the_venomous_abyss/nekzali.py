"""Nek'zali the Soulcoiler (The Venomous Abyss)."""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss


NEKZALI = RaidBoss(
    id=3470,
    name="Nek'zali the Soulcoiler",
    nick="Nek'zali",
    icon="inv_misc_questionmark.jpg",
)
boss = NEKZALI


################################################################################
# Trinkets


################################################################################
# Spells


boss.add_cast(
    spell_id=1292248,
    name="Soul Transfer",
    duration=15,
    color="rgb(49, 97, 72)",
    icon="ability_necrolord_fleshcraft.jpg",
)


boss.add_cast(
    spell_id=1289683,
    name="Ritual of Awakening",
    duration=20,
    color="rgb(161, 91, 66)",
    icon="inv_helm_mail_raidshamanmythic_s_01.jpg",
)


boss.add_cast(
    spell_id=1285681,
    name="Soulcoil Ignition",
    duration=4,
    color="rgb(116, 213, 242)",
    icon="spell_shadow_soulleech_2.jpg",
)


boss.add_cast(
    spell_id=1299673,
    name="Invoke",
    duration=5,
    color="rgb(204, 179, 155)",
    icon="warrior_disruptingshout.jpg",
)


boss.add_cast(
    spell_id=1284103,
    name="Possession Barrage",
    duration=6,
    color="rgb(127, 47, 173)",
    icon="spell_shadow_possession.jpg",
    show=True,
)
