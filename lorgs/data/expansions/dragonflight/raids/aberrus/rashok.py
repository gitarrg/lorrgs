"""05: Rashok, the Elder."""

from lorgs.models.raid_boss import RaidBoss


RASHOK = RaidBoss(
    id=2680,
    name="Rashok, the Elder",
    nick="Rashok",
    icon="inv_achievement_raiddragon_rashok.jpg",
)
boss = RASHOK

# Shadowlava Blast (406333) = Big Frontal
# small soak circles


# big leap
boss.add_cast(
    spell_id=405821,
    name="Charged Smash",
    duration=5,
    color="#b34747",
    icon="ability_shaman_lavalash.jpg",
)

# Group Soak
boss.add_cast(
    spell_id=400777,
    name="Charged Smash",
    duration=5,
    color="#bfaa32",
    icon="inv_shadowflame_missile.jpg",
)


# move to middle to drain energy
# (max 3x)
boss.add_buff(
    spell_id=401419,
    name="Elder's Conduit",
    color="#60b336",
    icon="spell_shadow_lifedrain02_purple.jpg",
)


# tank combo
# 3 casts of 2 spells
# Earthen Crush (407596)
# Flaming Slash (407544)
boss.add_cast(
    spell_id=407641,
    name="Wrath of Djaruun",
    duration=5,
    color="#478fb3",
    icon="inv_polearm_2h_dragonraid_d_02.jpg",
    show=False,
)
