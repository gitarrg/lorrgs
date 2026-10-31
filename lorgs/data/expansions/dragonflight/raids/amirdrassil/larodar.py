"""01: Gnarlroot."""

from lorgs.models.raid_boss import RaidBoss


LARODAR = RaidBoss(
    id=2731,
    name="Larodar, Keeper of the Flame",
    nick="Larodar",
    icon="inv_achievement_raidemeralddream_keeperoftheflames.jpg",
)
boss = LARODAR


################################################################################
# Phase 1

# Raging Inferno = big AOE?
boss.add_cast(
    spell_id=417634,
    name="Raging Inferno",
    duration=4 + 6,
    color="hsl(0, 50%, 50%)",
    icon="ability_mage_fierypayback.jpg",
)

# Treants Spawn?

# Roots

# Furious Outburst / Tank Charge = AoE
boss.add_cast(
    spell_id=425025,
    name="Furious Outburst",
    duration=4 + 6,
    color="hsl(220, 80%, 70%)",
    icon="spell_shaman_improvedfirenova.jpg",
)


# Everlasting Blaze = Small Orbs (Crit Buff)


################################################################################
# Intermission

# Cunsuming Flame = Intermission Cast
boss.add_cast(
    spell_id=421316,
    name="Consuming Flame",
    duration=2 + 16,
    color="hsl(120, 50%, 50%)",
    icon="ability_mage_burnout.jpg",
)


################################################################################
# Phase 2

# TODO: not

# Flash Fire = Heal Absorb + Spread
boss.add_cast(
    spell_id=427319,
    name="Flash Fire",
    duration=2 + 16,
    color="hsl(330, 70%, 65%)",
    icon="inv_misc_volatilefire.jpg",
)


# Smolering Backdraft = Tank Frontal
# applies Unnat style Health Leech
boss.add_cast(
    spell_id=429973,
    name="Smoldering Backdraft",
    duration=2.5,
    color="hsl(265, 70%, 70%)",
    icon="ability_racial_flayer.jpg",
)
