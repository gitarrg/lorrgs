"""06: The Vigilant Steward, Zskarn."""

from lorgs.models.raid_boss import RaidBoss


ZSKARN = RaidBoss(
    id=2689,
    name="The Vigilant Steward, Zskarn",
    nick="Zskarn",
    icon="inv_achievement_raiddragon_zskarn.jpg",
)
boss = ZSKARN


# Unstable Embers --> spread


# knockback
boss.add_cast(
    spell_id=403978,
    name="Blast Wave",
    duration=3,
    icon="ability_foundryraid_blastwave.jpg",
    color="#b04a4a",
)

# full energy --> activate statues
boss.add_cast(
    spell_id=406678,
    name="Tactical Destruction",
    duration=3,
    icon="spell_fire_ragnaros_molteninferno.jpg",
    color="#4dab46",
)


# spawn adds
boss.add_cast(
    spell_id=405812,
    name="Animate Golems",
    duration=3,
    icon="achievement_dungeon_ulduarraid_irongolem_01.jpg",
    color="#e3c714",
)


# tank --> soak bombs
boss.add_cast(
    spell_id=406725,
    name="Shrapnel Bomb",
    icon="ability_hunter_traplauncher.jpg",
    color="#478fb3",
    show=False,
)
