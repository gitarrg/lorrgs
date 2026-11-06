"""Define the Paladin Class and its Specs (WoW Forever)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.forever.roles import HEAL, MDPS, TANK
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


################################################################################
# Class
#
PALADIN = WowClass(id=2, name="Paladin", color="#F48CBA", talent_tree_id=1100)

################################################################################
# Specs
#
PALADIN_HOLY = WowSpec(id=65, index=1, role=HEAL, wow_class=PALADIN, name="Holy")
PALADIN_PROTECTION = WowSpec(id=66, index=2, role=TANK, wow_class=PALADIN, name="Protection", short_name="Prot")
PALADIN_RETRIBUTION = WowSpec(id=70, index=3, role=MDPS, wow_class=PALADIN, name="Retribution", short_name="Ret")

################################################################################
# Spells
#
# Spellbook
# A targeted party member is protected from all physical attacks for 10 sec, but during that time they cannot
# attack or use physical abilities. Players may only have one Blessing on them per Paladin at any one time.
# Applies Forbearance for 1 min. Cannot be cast while Forbearance is active.
PALADIN.add_spell(spell_id=10278, cooldown=300, duration=10, name="Blessing of Protection", icon="spell_holy_sealofprotection.jpg", show=False)

# The paladin sacrifices himself to remove the targeted party member from harms way. Enemies will stop attacking
# the protected party member, who will be immune to all harmful attacks but cannot take any action for 3 min.
# PALADIN.add_spell(spell_id=19752, cooldown=3600, duration=180, name="Divine Intervention", icon="spell_nature_timestop.jpg")

# You are protected from all physical attacks and spells for 8 sec, but during that time you cannot attack or
# use physical abilities yourself. Applies Forbearance for 1 min. Cannot be cast while Forbearance is active.
PALADIN.add_spell(spell_id=5573, cooldown=300, duration=8, name="Divine Protection", icon="spell_holy_restoration.jpg", show=False)

# Protects the paladin from all damage and spells for 12 sec, but reduces all damage you deal by 50%. Applies
# Forbearance for 1 min. Cannot be cast while Forbearance is active.
PALADIN.add_spell(spell_id=1020, cooldown=300, duration=12, name="Divine Shield", icon="spell_holy_divineintervention.jpg", show=False)

# Heals a friendly target for an amount equal to the Paladin's maximum health and restores 550 of their mana.
# Drains all of the Paladin's remaining Mana when used, but does not interrupt Mana regeneration.
PALADIN.add_spell(spell_id=10310, cooldown=1200, name="Lay on Hands", icon="spell_holy_layonhands.jpg")

# Grants you immunity to Silence and Interrupt effects for 6 sec.
PALADIN.add_spell(spell_id=1310897, cooldown=180, duration=6, name="Voice of Truth", icon="inv_misc_horn_03.jpg")

# Talents: Holy
# When activated, gives your next Flash of Light, Holy Light, or Holy Shock spell a 100% critical effect chance.
PALADIN_HOLY.add_spell(spell_id=20216, cooldown=120, name="Divine Favor", icon="spell_holy_heal.jpg")

# Talents: Protection
# When activated, this ability grants you an absorb shield equal to 100% of your maximum health for 8 sec.
# Applies Forbearance for 1 min. Cannot be cast while Forbearance is active.
PALADIN_PROTECTION.add_spell(spell_id=1311015, cooldown=300, duration=8, name="Templar's Bulwark", icon="ability_paladin_shieldofthetemplar.jpg", show=False)
