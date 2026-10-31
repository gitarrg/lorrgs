"""01: Gnarlroot."""

from lorgs.models.raid_boss import RaidBoss


TINDRAL = RaidBoss(
    id=2786,
    name="Tindral Sageswift, Seer of the Flame",
    nick="Tindral",
    icon="inv_achievement_raidemeralddream_druidoftheflame.jpg",
)
boss = TINDRAL


################################################################################
# Main Phases
################################################################################

# Flaming Germination = big AOE
boss.add_cast(
    spell_id=423265,
    name="Flaming Germination",
    duration=10,
    color="hsl(0, 50%, 50%)",
    icon="ability_warlock_inferno.jpg",
)


boss.add_cast(
    spell_id=421398,
    name="Fire Beam",
    duration=2,
    color="hsl(45, 75%, 50%)",
    icon="ability_mage_firestarter.jpg",
    show=False,
)


boss.add_cast(
    spell_id=424495,
    name="Mass Entanglement",
    duration=5,  # duration not fixed.
    color="hsl(30, 50%, 60%)",
    icon="10_2_raidability_burningroots.jpg",
)


boss.add_cast(
    spell_id=424581,
    name="Fiery Growth",
    duration=12,  # aprox 3x4sec between the dispells
    color="hsl(270, 50%, 60%)",
    icon="spell_burningsoul.jpg",
)


boss.add_cast(
    spell_id=420236,
    name="Falling Star",
    duration=2,
    color="hsl(240, 80%, 70%)",
    icon="ability_druid_starfall.jpg",
    show=False,
)


# Wild Mushrooms = Tank Soak?
boss.add_cast(
    spell_id=423260,
    name="Blazing Mushroom",
    duration=1.5 + 9,  # duration not fixed.
    color="hsl(220, 80%, 70%)",
    icon="spell_druid_wildmushroom_frenzy.jpg",
    variations=[
        426669,  # Mythic Spell ID
    ],
)


################################################################################
# Intermissions
################################################################################

boss.add_buff(
    spell_id=421603,
    name="Incarnation: Owl of the Flame",
    color="hsl(120, 50%, 50%)",
    icon="inv_dreamowl_firemount.jpg",
)

# Supernova = Shield + AoE
boss.add_buff(
    spell_id=424140,
    name="Supernova",
    color="hsl(340, 70%, 50%)",
    icon="spell_fire_felflamering_red.jpg",
)
