"""Define the Hunter Class and its Specs (WoW Forever)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.forever.roles import RDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


################################################################################
# Class
#
HUNTER = WowClass(id=3, name="Hunter", color="#AAD372", talent_tree_id=1091)

################################################################################
# Specs
#
HUNTER_BEASTMASTERY = WowSpec(id=253, index=1, role=RDPS, wow_class=HUNTER, name="Beast Mastery")
HUNTER_MARKSMANSHIP = WowSpec(id=254, index=2, role=RDPS, wow_class=HUNTER, name="Marksmanship")
HUNTER_SURVIVAL = WowSpec(id=255, index=3, role=RDPS, wow_class=HUNTER, name="Survival")

################################################################################
# Spells
#
# Spellbook
# Increases ranged and melee attack speed by 40% for 15 sec.
HUNTER.add_spell(spell_id=3045, cooldown=300, duration=15, name="Rapid Fire", icon="ability_hunter_runningshot.jpg")

# Talents: Beast Mastery
# Send your pet into a rage causing 50% additional damage for 18 sec. While enraged, the beast does not feel
# pity or remorse or fear and it cannot be stopped unless killed.
HUNTER_BEASTMASTERY.add_spell(spell_id=19574, cooldown=120, duration=18, name="Bestial Wrath", icon="ability_druid_ferociousbite.jpg")

# Talents: Survival
# When activated, increases your Dodge and Parry chance by 25% for 10 sec.
HUNTER_SURVIVAL.add_spell(spell_id=19263, cooldown=300, duration=10, name="Deterrence", icon="ability_whirlwind.jpg")
