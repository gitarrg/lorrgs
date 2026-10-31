"""02: The Bloodbound Horror."""

from lorgs.models.raid_boss import RaidBoss


BLOODBOUND_HORROR = RaidBoss(
    id=2917,
    name="The Bloodbound Horror",
    nick="Bloodbound Horror",
    icon="inv_achievement_raidnerubian_blackblood.jpg",
)
boss = BLOODBOUND_HORROR


# Tank Frontal --> go into zone (Anduin)
#     Gruesome Disgorge (5sec cast + initial)
#     Baneful Shift (40sec dot)
boss.add_cast(
    spell_id=444363,
    name="Gruesome Disgorge",
    duration=5,  # 5sec cast
    cooldown=40,  # 40sec debuff
    color="hsl(120, 50%, 50%)",
    icon="ability_warlock_shadowflame.jpg",
)


# 100% Energy = big blue circle / run out. Does AOE
boss.add_cast(
    spell_id=442530,
    name="Goresplatter",
    duration=8,
    cooldown=10,
    color="hsl(0, 50%, 50%)",
    icon="spell_shadow_corpseexplode.jpg",
)

"""
# Adds:
    - Lost Watcher
    - needs tank
    - channel gives shield to boss

    - Forgotten Harbringr
        summon small adds
        --> small adds try to reach boss. Kill them!
"""
