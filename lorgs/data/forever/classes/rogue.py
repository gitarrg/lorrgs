"""Define the Rogue Class and its Specs (WoW Forever)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.forever.roles import MDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


################################################################################
# Class
#
ROGUE = WowClass(id=4, name="Rogue", color="#FFF468", talent_tree_id=1111)

################################################################################
# Specs
#
ROGUE_ASSASSINATION = WowSpec(id=259, index=1, role=MDPS, wow_class=ROGUE, name="Assassination", short_name="Assa")
ROGUE_COMBAT = WowSpec(id=260, index=2, role=MDPS, wow_class=ROGUE, name="Combat")
ROGUE_SUBTLETY = WowSpec(id=261, index=3, role=MDPS, wow_class=ROGUE, name="Subtlety")

################################################################################
# Spells
#
# Spellbook

# Blinds the target, causing it to wander disoriented for up to 10 sec. Any damage caused will remove the
# effect.
# ROGUE.add_spell(spell_id=2094, cooldown=300, duration=10, name="Blind", icon="spell_shadow_mindsteal.jpg")

# The rogue's dodge chance will increase by 50% for 15 sec.
ROGUE.add_spell(spell_id=5277, cooldown=300, duration=15, name="Evasion", icon="spell_shadow_shadowward.jpg", show=False)

# Increases the rogue's movement speed by 70% for 15 sec. Does not break stealth.
# ROGUE.add_spell(spell_id=11305, cooldown=300, duration=15, name="Sprint", icon="ability_rogue_sprint.jpg")

# Allows the rogue to vanish from sight, entering an improved stealth mode for 10 sec. Also breaks movement
# impairing effects. More effective than Vanish (Rank 1).
# ROGUE.add_spell(spell_id=1857, cooldown=300, duration=10, name="Vanish", icon="ability_vanish.jpg")

# Talents: Assassination
# When activated, increases the critical strike chance of your next Sinister Strike, Backstab, Ambush,
# Eviscerate, or Mutilate by 100%.
ROGUE_ASSASSINATION.add_spell(spell_id=14177, cooldown=180, name="Cold Blood", icon="spell_ice_lament.jpg")

# Talents: Combat
# Increases your melee attack speed by 20% and your melee attacks strike an additional nearby opponent. Lasts 15
# sec.
ROGUE_COMBAT.add_spell(spell_id=13877, cooldown=120, duration=15, name="Blade Flurry", icon="ability_warrior_punishingblow.jpg")
# Increases your Energy regeneration rate by 100% for 15 sec.
ROGUE_COMBAT.add_spell(spell_id=13750, cooldown=300, duration=15, name="Adrenaline Rush", icon="spell_shadow_shadowworddominate.jpg")

# Talents: Subtlety
# Adds 2 Combo Points to your target. You must add to or use those combo points within 20 sec or the combo
# points are lost.
ROGUE_SUBTLETY.add_spell(spell_id=14183, cooldown=120, duration=20, name="Premeditation", icon="spell_shadow_possession.jpg")
# When activated, this ability immediately finishes the cooldown on your other Rogue abilities.
ROGUE_SUBTLETY.add_spell(spell_id=14185, cooldown=600, name="Preparation", icon="spell_shadow_antishadow.jpg")
