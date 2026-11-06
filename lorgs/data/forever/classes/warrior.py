"""Define the Warrior Class and its Specs (WoW Forever)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.forever.roles import MDPS, TANK
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


################################################################################
# Class
#
WARRIOR = WowClass(id=1, name="Warrior", color="#C69B6D", talent_tree_id=1117)

################################################################################
# Specs
#
WARRIOR_ARMS = WowSpec(id=71, index=1, role=MDPS, wow_class=WARRIOR, name="Arms")
WARRIOR_FURY = WowSpec(id=72, index=2, role=MDPS, wow_class=WARRIOR, name="Fury")
WARRIOR_PROTECTION = WowSpec(id=73, index=3, role=TANK, wow_class=WARRIOR, name="Protection", short_name="Prot")

################################################################################
# Spells
#
# Generates 10 rage at the cost of health, and then generates an additional 10 rage over 10 sec.
WARRIOR.add_spell(spell_id=2687, cooldown=60, duration=10, name="Bloodrage", icon="ability_racial_bloodrage.jpg")

# Spellbook
# Forces all nearby enemies within 10 yards to focus attacks on you for 6 sec.
WARRIOR.add_spell(spell_id=1161, cooldown=600, duration=6, name="Challenging Shout", icon="ability_bullrush.jpg")
# The warrior shouts, causing the targeted enemy to cower in fear. Up to 5 enemies within 8 yds will flee in
# fear. Lasts 8 sec.
WARRIOR.add_spell(spell_id=5246, cooldown=180, duration=8, name="Intimidating Shout", icon="ability_golemthunderclap.jpg")
# A mocking attack that causes 93 damage, a moderate amount of threat and forces the target to focus attacks on
# you for 6 sec.
WARRIOR.add_spell(spell_id=20560, cooldown=120, duration=6, name="Mocking Blow", icon="ability_warrior_punishingblow.jpg")
# The warrior will gain 100% increased critical strike chance and will be immune to Fear effects for the next 15
# sec, but all damage taken is increased by 20%.
WARRIOR.add_spell(spell_id=1719, cooldown=1800, duration=15, name="Recklessness", icon="ability_criticalstrike.jpg")
# Instantly counterattack any enemy that strikes you in melee for 15 sec. Melee attacks made from behind cannot
# be counterattacked. A maximum of 30 attacks will cause retaliation.
WARRIOR.add_spell(spell_id=20230, cooldown=900, duration=15, name="Retaliation", icon="ability_warrior_challange.jpg")
# Reduces the damage taken from all attacks by 60% for 12 sec.
WARRIOR.add_spell(spell_id=871, cooldown=900, duration=12, name="Shield Wall", icon="ability_warrior_shieldwall.jpg")

# Talents: Fury
# When activated, increases your Physical damage done by 20% and makes you immune to Fear effects, but increases
# all damage you take by 5%. Lasts 30 sec.
WARRIOR_FURY.add_spell(spell_id=12328, cooldown=180, duration=30, name="Death Wish", icon="spell_shadow_deathpact.jpg")

# Talents: Protection
# When activated, this ability temporarily grants you 30% of your maximum health for 20 sec. After the effect
# expires, the health is lost.
WARRIOR_PROTECTION.add_spell(spell_id=12975, cooldown=180, duration=20, name="Last Stand", icon="spell_holy_ashestoashes.jpg")
