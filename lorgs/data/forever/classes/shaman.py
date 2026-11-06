"""Define the Shaman Class and its Specs (WoW Forever)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.forever.roles import HEAL, MDPS, RDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


################################################################################
# Class
#
SHAMAN = WowClass(id=7, name="Shaman", color="#0070DD", talent_tree_id=1082)

################################################################################
# Specs
#
SHAMAN_ELEMENTAL = WowSpec(id=262, index=1, role=RDPS, wow_class=SHAMAN, name="Elemental")
SHAMAN_ENHANCEMENT = WowSpec(id=263, index=2, role=MDPS, wow_class=SHAMAN, name="Enhancement")
SHAMAN_RESTORATION = WowSpec(id=264, index=3, role=HEAL, wow_class=SHAMAN, name="Restoration", short_name="Resto")

################################################################################
# Spells
#
# Spellbook
# Yanks the caster through the twisting nether back to Hearthstone Location. Speak to an Innkeeper in a
# different place to change your home location.
# SHAMAN.add_spell(spell_id=556, cooldown=900, name="Astral Recall", icon="spell_nature_astralrecal.jpg")

# Allows you to resurrect yourself upon death with 20% health and mana.
# SHAMAN.add_spell(spell_id=20608, cooldown=3600, name="Reincarnation", icon="spell_nature_reincarnation.jpg")

# Talents: Elemental
# Gain mastery over Lightning, reducing the cast time of your Lightning Bolt spell by 0.5 sec, and removing the
# cooldown from your Chain Lightning spell. Lasts 15 sec.
SHAMAN_ELEMENTAL.add_spell(spell_id=16166, cooldown=180, duration=15, name="Lightning Mastery", icon="spell_nature_unrelentingstorm.jpg")

# Talents: Enhancement
# Increases your attack speed by 30% for 25 sec.
SHAMAN_ENHANCEMENT.add_spell(spell_id=425336, cooldown=180, duration=25, name="Rage of the Farseer", icon="spell_nature_bloodlust.jpg")

# Talents: Restoration
# Summons a Mana Tide Totem with 5 health at the feet of the caster for 12 sec that restores 290 mana every 3
# seconds to group members within 30 yards.
SHAMAN_RESTORATION.add_spell(spell_id=1325256, cooldown=300, duration=13, name="Mana Tide Totem", icon="spell_frost_summonwaterelemental.jpg")
# When activated, your next Nature spell with a casting time less than 10 sec. becomes an instant cast spell.
SHAMAN_RESTORATION.add_spell(spell_id=16188, cooldown=180, name="Nature's Swiftness", icon="spell_nature_ravenform.jpg")
