"""04: Sennarth, The Cold Breath."""

from lorgs.models.raid_boss import RaidBoss


SENNARTH = RaidBoss(
    id=2592,
    name="Sennarth, The Cold Breath",
    nick="Sennarth",
    icon="achievement_raidprimalist_sennarth.jpg",
)


##############
# P1

# Spread Debuffs
SENNARTH.add_cast(
    spell_id=371976,
    name="Chilling Blast",
    duration=2 + 5,
    color="#2996cc",
    icon="spell_fire_blueflamering.jpg",
)


# Big Add AoE
SENNARTH.add_cast(
    spell_id=373817,
    name="Chilling Aura",
    duration=2 + 5,
    color="#45e6cb",
    icon="spell_frost_coldhearted.jpg",
)

# Grip
SENNARTH.add_cast(
    spell_id=373405,
    name="Gossamer Burst",
    duration=3 + 6,
    color="#ffd500",
    icon="priest_icon_chakra.jpg",
)


# Spiders
SENNARTH.add_cast(
    spell_id=372238,
    name="Call Spiderlings",
    duration=9,
    color="#60bf30",
    icon="inv_misc_monsterspidercarapace_01.jpg",
    show=False,
)

# Web
SENNARTH.add_cast(
    spell_id=372082,
    name="Enveloping Webs",
    duration=1 + 6,
    show=False,
    color="#af60bf",
    icon="inv_misc_web_01.jpg",
)


##############
# P2

# Enrage
SENNARTH.add_cast(
    spell_id=372648,
    name="Pervasive Cold",
    duration=6,
    color="#bf3030",
    icon="ability_mage_chilledtothebone.jpg",
)

# Knockback
SENNARTH.add_cast(
    spell_id=373027,
    name="Suffocating Webs",
    duration=3 + 6,
    color="#af60bf",
    icon="inv_misc_web_02.jpg",
)
