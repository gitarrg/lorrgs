"""01: Gnarlroot."""

from lorgs.data.constants import COL_GREEN_1, COL_ORANGE_1, COL_PURPLE_1, COL_RED_1
from lorgs.models.raid_boss import RaidBoss


IGIRA = RaidBoss(
    id=2709,
    name="Igira the Cruel",
    nick="Igira",
    icon="inv_achievement_raidemeralddream_igira-the-cruel.jpg",
)
boss = IGIRA


################################################################################
# Base Spells
# Spear Circles
# Frontal (hide=True)


################################################################################
# "Phases"
# Full Energy => Knock --> choose ability
boss.add_cast(
    spell_id=422776,
    name="Marked for Torment",
    duration=1.6,
    color=COL_GREEN_1,
    icon="ability_mage_tormentoftheweak.jpg",
)


# Axe / Group Soak
boss.add_cast(
    spell_id=416048,
    name="Umbral Destruction",
    duration=4.5,
    color=COL_RED_1,
    icon="inv_legendary_axe.jpg",
)

# Sword / Leap
boss.add_cast(
    spell_id=418531,
    name="Smashing Viscera",
    duration=3,
    color=COL_ORANGE_1,
    icon="inv_legendary_sword.jpg",
)

# Spear = Heal Absorb
boss.add_cast(
    spell_id=415624,
    name="Heart Stopper",
    duration=1.5,
    color=COL_PURPLE_1,
    icon="ui_venthyranimaboss_heartsword.jpg",
)
