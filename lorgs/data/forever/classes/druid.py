"""Define the Druid Class and its Specs (WoW Forever)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.forever.roles import HEAL, MDPS, RDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


################################################################################
# Class
#
DRUID = WowClass(id=11, name="Druid", color="#FF7C0A", talent_tree_id=1089)

################################################################################
# Specs
#
DRUID_BALANCE = WowSpec(id=102, index=1, role=RDPS, wow_class=DRUID, name="Balance")
DRUID_FERAL = WowSpec(id=103, index=2, role=MDPS, wow_class=DRUID, name="Feral")
DRUID_RESTORATION = WowSpec(id=105, index=3, role=HEAL, wow_class=DRUID, name="Restoration", short_name="Resto")

################################################################################
# Spells
#
# Spellbook
# Forces all nearby enemies to focus attacks on you for 6 sec.
DRUID.add_spell(spell_id=5209, cooldown=600, duration=6, name="Challenging Roar", icon="ability_druid_challangingroar.jpg")

# Increases movement speed by 60% for 15 sec. Does not break prowling.
DRUID.add_spell(spell_id=9821, cooldown=300, duration=15, name="Dash", icon="ability_druid_dash.jpg", show=False)

# Converts up to 10 Rage per second into health for 10 sec. Each point of Rage is converted into 1% health.
DRUID.add_spell(spell_id=22842, cooldown=180, duration=10, name="Frenzied Regeneration", icon="ability_bullrush.jpg", show=False)

# Returns the spirit to the body, restoring a dead target to life with 2200 health and 2800 mana.
# DRUID.add_spell(spell_id=20748, cooldown=1800, name="Rebirth", icon="spell_nature_reincarnation.jpg", show=False)

# Regenerates all nearby party members within 20 yards for 291 every 2 sec for 10 sec. Druid must channel to
# maintain the spell.
DRUID.add_spell(spell_id=9863, cooldown=300, duration=10, name="Tranquility", icon="spell_nature_tranquility.jpg")

# Talents: Restoration
# When activated, your next Nature spell becomes an instant cast spell.
DRUID_RESTORATION.add_spell(spell_id=17116, cooldown=180, name="Nature's Swiftness", icon="spell_nature_ravenform.jpg")
