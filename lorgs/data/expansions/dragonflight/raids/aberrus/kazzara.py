"""01: Kazzara, the Hellforged."""

from lorgs.models.raid_boss import RaidBoss


KAZZARA = RaidBoss(
    id=2688,
    name="Kazzara, the Hellforged",
    nick="Kazzara",
    icon="inv_achievement_raiddragon_kazzara.jpg",
)
boss = KAZZARA


# Pools and Lasers
boss.add_cast(
    spell_id=407196,
    name="Dread Rifts",
    icon="inv_shadowflame_groundstate.jpg",
    color="#e68a2e",
    show=False,
)

boss.add_cast(
    spell_id=407069,
    name="Rays of Anguish",
    icon="ability_mage_firestarter.jpg",
    color="#e6c72e",
    show=False,
)


# Pushback
boss.add_cast(
    spell_id=403326,
    name="Wings of Extinction",
    duration=20,
    color="#8f3f3f",
    icon="inv_icon_wingbroken07d.jpg",
)

# Phases
boss.add_cast(
    spell_id=401316,
    name="Hellsteel Carnage",
    duration=3,
    color="#60b336",
    icon="achievment_boss_spineofdeathwing.jpg",
    variations=[401318, 401319],
)


# Tank Hit
boss.add_cast(
    spell_id=404744,
    name="Terror Claws",
    duration=25,
    show=False,
    color="#478fb3",
    icon="inv_10_elementalshardfoozles_shadowflame.jpg",
)
