"""Define the Warlock Class and its Specs (WoW Forever)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.forever.roles import RDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


################################################################################
# Class
#
WARLOCK = WowClass(id=9, name="Warlock", color="#8788EE", talent_tree_id=1116)

################################################################################
# Specs
#
WARLOCK_AFFLICTION = WowSpec(id=265, index=1, role=RDPS, wow_class=WARLOCK, name="Affliction", short_name="Aff")
WARLOCK_DEMONOLOGY = WowSpec(id=266, index=2, role=RDPS, wow_class=WARLOCK, name="Demonology", short_name="Demo")
WARLOCK_DESTRUCTION = WowSpec(id=267, index=3, role=RDPS, wow_class=WARLOCK, name="Destruction", short_name="Destro")

################################################################################
# Spells
#

# Causes the enemy target to run in horror for 3 sec and causes 472 Shadow damage. The caster gains 100% of the
# damage caused in health.
# WARLOCK.add_spell(spell_id=17926, cooldown=120, duration=3, name="Death Coil", icon="spell_shadow_deathcoil.jpg")

# Summons a meteor from the Twisting Nether, causing 200 Fire damage and stunning all enemy targets in the area
# for 2 sec. An Infernal rises from the crater, under the command of the caster for 5 min. Once control is lost,
# the Infernal must be Subjugated to maintain control. Can only be used outdoors.
WARLOCK.add_spell(spell_id=1122, cooldown=3600, duration=15, name="Inferno", icon="spell_shadow_summoninfernal.jpg")

# Begins a ritual that sacrifices a random participant to summon a doomguard. The doomguard must be immediately
# subjugated or it will attack the ritual participants. Requires the caster and 4 additional party members to
# complete the ritual. In order to participate, all players must right-click the portal and not move until the
# ritual is complete.
# WARLOCK.add_spell(spell_id=18540, cooldown=3600, duration=60, name="Ritual of Doom", icon="spell_shadow_antimagicshell.jpg")

# Talents: Affliction
# Increases the effect of your next Curse of Weakness or Bane of Agony by 50%, or your next Curse of Exhaustion
# by 20%. Lasts 30 sec.
WARLOCK_AFFLICTION.add_spell(spell_id=18288, cooldown=180, duration=30, name="Amplify Curse", icon="spell_shadow_contagion.jpg")

# Talents: Demonology
# Your next Imp, Voidwalker, Succubus, Incubus, or Felhunter Summon spell has its casting time reduced by 6 sec
# and its Mana cost reduced by 50%.
# WARLOCK_DEMONOLOGY.add_spell(spell_id=18708, cooldown=300, duration=15, name="Fel Domination", icon="spell_nature_removecurse.jpg")
