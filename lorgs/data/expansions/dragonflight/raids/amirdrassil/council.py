"""01: Gnarlroot."""

from lorgs.models.raid_boss import RaidBoss


COUNCIL_OF_DREAMS = RaidBoss(
    id=2728,
    name="Council of Dreams",
    icon="inv_achievement_raidemeralddream_dreamcouncil.jpg",
)
boss = COUNCIL_OF_DREAMS


####################################
# Urctos
boss.add_cast(
    spell_id=420525,
    name="Blind Rage",
    duration=2.5 + 10,
    color="hsl(330, 60%, 60%)",
    icon="spell_winston_rage.jpg",
)

boss.add_cast(
    spell_id=420947,
    name="Barreling Charge",
    duration=2.5 + 10,
    color="hsl(10, 60%, 55%)",
    icon="ability_xavius_tormentingswipe.jpg",
)


boss.add_cast(
    spell_id=421020,
    name="Agonizing Claws",
    duration=18,
    color="#478fb3",
    icon="spell_druid_bloodythrash.jpg",
    show=False,
)


####################################
# Aerwynn

boss.add_cast(
    spell_id=421292,
    name="Constricting Thicket",
    duration=4 + 18,
    color="hsl(90, 60%, 55%)",
    icon="spell_nature_stranglevines.jpg",
)


####################################
# Pip

boss.add_cast(
    spell_id=421029,
    name="Song of the Dragon",
    duration=6,
    color="hsl(45, 85%, 70%)",
    icon="inv_misc_firedancer_01.jpg",
)

boss.add_cast(
    spell_id=418757,
    name="Polymorph Bomb",
    duration=12,
    color="hsl(270, 85%, 70%)",
    icon="inv_duckbaby_mallard.jpg",
)
