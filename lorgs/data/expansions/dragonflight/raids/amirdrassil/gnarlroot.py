"""01: Gnarlroot."""

from lorgs.models.raid_boss import RaidBoss


GNARLROOT = RaidBoss(
    id=2820,
    name="Gnarlroot",
    icon="inv_achievement_raidemeralddream_fieryancient.jpg",
)
boss = GNARLROOT


################################################################################
# Phase 1
#

# Adds Spawn
# --> Circle debuff > trigger adds


# 4x per Phase: 0:10, 0:40, 1:05, 1:30
boss.add_cast(
    spell_id=422026,
    name="Tortured Scream",
    duration=2.5 + 10,
    color="#7b47bf",
    icon="ability_soulrenderdormazain_hellscream.jpg",
)


boss.add_cast(
    spell_id=424352,
    name="Dreadfire Barrage",
    duration=4,
    color="#478fb3",
    icon="inv_shadowflame_buff.jpg",
    show=False,
)


################################################################################
# Phase 2
#
# soak circles --> break roots
# --> 20sec burn

boss.add_buff(
    spell_id=421013,
    name="Doom Cultivation",
    color="#60b336",
    icon="trade_herbalism.jpg",
)

boss.add_debuff(
    spell_id=421840,
    name="Uprooted Agony",
    duration=20,
    color="#c53838",
    icon="inv_shadowflame_debuff.jpg",
)
