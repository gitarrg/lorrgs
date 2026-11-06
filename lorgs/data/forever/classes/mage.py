"""Define the Mage Class and its Specs (WoW Forever)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.forever.roles import RDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


################################################################################
# Class
#
MAGE = WowClass(id=8, name="Mage", color="#3FC7EB", talent_tree_id=1112)

################################################################################
# Specs
#
MAGE_ARCANE = WowSpec(id=62, index=1, role=RDPS, wow_class=MAGE, name="Arcane")
MAGE_FIRE = WowSpec(id=63, index=2, role=RDPS, wow_class=MAGE, name="Fire")
MAGE_FROST = WowSpec(id=64, index=3, role=RDPS, wow_class=MAGE, name="Frost")

################################################################################
# Spells
#
# Spellbook
# While channeling this spell, your mana regeneration is active and increased by 1500%. Lasts 8 sec.
MAGE.add_spell(spell_id=12051, cooldown=480, duration=8, name="Evocation", icon="spell_nature_purge.jpg")

# Talents: Arcane
# When activated, your next Mage spell with a casting time less than 10 sec becomes an instant cast spell.
MAGE_ARCANE.add_spell(spell_id=12043, cooldown=180, name="Presence of Mind", icon="spell_nature_enchantarmor.jpg")
# For the next 15 sec, your spells deal 30% more damage while costing 30% more mana to cast.
MAGE_ARCANE.add_spell(spell_id=12042, cooldown=180, duration=15, name="Arcane Power", icon="spell_nature_lightning.jpg")

# Talents: Fire
# When activated, this spell causes each of your Fire damage spell hits to increase your critical strike chance
# with Fire damage spells by 10%. This effect lasts until you have caused 3 non-periodic critical strikes with
# Fire spells.
MAGE_FIRE.add_spell(spell_id=11129, cooldown=180, name="Combustion", icon="spell_fire_sealoffire.jpg")

# Talents: Frost
# You become encased in a block of ice, protecting you from all physical attacks and spells for 10 sec, but
# during that time you cannot attack, move, or cast spells.
MAGE_FROST.add_spell(spell_id=11958, cooldown=300, duration=10, name="Ice Block", icon="spell_frost_frost.jpg")
# Finishes the remaining cooldown on all your other Frost spells.
MAGE_FROST.add_spell(spell_id=12472, cooldown=600, name="Cold Snap", icon="spell_frost_wizardmark.jpg")
