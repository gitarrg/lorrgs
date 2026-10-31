"""07: Magmorax."""

from lorgs.models.raid_boss import RaidBoss


MAGMORAX = RaidBoss(
    id=2683,
    name="Magmorax",
    icon="inv_achievement_raiddragon_magmorax.jpg",
)
boss = MAGMORAX


# player debuffs -> spawn puddles
boss.add_cast(
    spell_id=402989,
    name="Molten Spittle",
    duration=1.5 + 6,
    color="#9669d1",
    icon="spell_fire_firebolt02.jpg",
)

# random puddles
boss.add_cast(
    spell_id=403740,
    name="Igniting Roar",
    duration=2.5,
    color="#bf3030",
    icon="inv_misc_head_dragon_01.jpg",
)

# knockback
boss.add_cast(
    spell_id=403671,
    name="Overpowering Stomp",
    duration=4,
    color="#bf8330",
    icon="spell_nature_earthquake.jpg",
)


# Tank Hit
boss.add_cast(
    spell_id=404846,
    name="Incinerating Maws",
    duration=1.5,
    color="#2695d1",
    icon="spell_fire_burnout.jpg",
    show=False,
)
