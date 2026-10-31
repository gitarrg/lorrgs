"""03: Sikran."""

from lorgs.models.raid_boss import RaidBoss


SIKRAN = RaidBoss(
    id=2898,
    name="Sikran, Captain of the Sureki",
    nick="Sikran",
    icon="inv_achievement_raidnerubian_nerubianevolved.jpg",
)
boss = SIKRAN


# charge on random players --> leaves images + dot
boss.add_cast(
    spell_id=433519,
    name="Phase Blades",
    duration=1.5,
    cooldown=20,  # dot
    color="hsl(0, 50%, 50%)",
    icon="ability_warrior_shieldcharge.jpg",
)


# beams on random players --> use to destroy images
boss.add_cast(
    spell_id=442428,
    name="Decimate",
    duration=2,
    color="hsl(90, 60%, 55%)",
    icon="inv_polearm_2h_nerubianraid_d_01.jpg",
)


# boss destorys all images at full energy --> lots of dmg
boss.add_cast(
    spell_id=456420,
    name="Shattering Sweep",
    duration=5,
    color="hsl(270, 50%, 60%)",
    icon="inv_sword_48.jpg",
)


boss.add_cast(
    spell_id=435403,
    name="Phase Lunge",
    duration=30,
    color="#478fb3",
    icon="inv_sword_1h_nerubianraid_d_01.jpg",
    show=False,
)
