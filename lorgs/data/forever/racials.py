"""Racials with a cooldown over 60 sec (WoW Forever).

Ref: https://www.wowhead.com/forever/talent-calc (racials of each class).
Races 95 and 96 are Forever's own races (Warcraft Logs and Wowhead have no names for them yet).
"""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.forever.classes.other import OTHER_RACIALS
from lorgs.data.forever.roles import ALL_ROLES


################################################################################
# Human

# Dramatically increases stealth detection for 20 sec.
# OTHER_RACIALS.add_spell(spell_id=20600, cooldown=180, duration=20, name="Perception", icon="spell_nature_sleep.jpg")

# Instantly removes all Stun effects.
# OTHER_RACIALS.add_spell(spell_id=1259718, cooldown=180, name="Will to Survive", icon="spell_shadow_charm.jpg")

################################################################################
# Orc

# Increases Attack Power and Spell Power by 10% for 15 sec.
OTHER_RACIALS.add_spell(spell_id=20572, cooldown=120, duration=15, name="Blood Fury", icon="racial_orc_berserkerstrength.jpg")

# Instantly removes all Curses and Banes, and reduces all Magical damage taken by 5% for 8 sec.
# OTHER_RACIALS.add_spell(spell_id=1299026, cooldown=180, duration=8, name="Shatter Curse", icon="spell_nature_removecurse.jpg")

################################################################################
# Dwarf
# Instantly removes and grants immunity to all Bleed, Poison, and Disease effects, and reduces all Physical
# damage taken by 10% for 8 sec.
# OTHER_RACIALS.add_spell(spell_id=20594, cooldown=180, duration=8, name="Stoneform", icon="spell_shadow_unholystrength.jpg")

################################################################################
# Night Elf

# Increases your critical strike chance with all spells and attacks by 10% for 15 sec.
OTHER_RACIALS.add_spell(spell_id=1259799, cooldown=180, duration=15, name="Elune's Light", icon="spell_nature_moonglow.jpg")

################################################################################
# Undead

# When activated, regenerates 7% of total Health and 7% of total Mana every 2 sec for 10 sec. Only works on
# Humanoid or Undead corpses within 5 yds. Any movement, action, or damage taken while Cannibalizing will cancel
# the effect.
# OTHER_RACIALS.add_spell(spell_id=20577, cooldown=120, duration=10, name="Cannibalize", icon="ability_racial_cannibalize.jpg")

# Undead
# Instantly removes all Charm, Fear and Sleep effects.
OTHER_RACIALS.add_spell(spell_id=7744, cooldown=120, name="Will of the Forsaken", icon="spell_shadow_raisedead.jpg")

################################################################################
# Tauren
# Cultivate a nearby herb, growing a duplicate you can harvest without requiring Herbalism skill. Each herb may
# only be cultivated once.
# OTHER_RACIALS.add_spell(spell_id=20552, cooldown=900, name="Cultivation", icon="inv_misc_flower_01.jpg")

# Tauren
# Stuns up to 5 enemies within 8 yds for 2 sec.
# OTHER_RACIALS.add_spell(spell_id=20549, cooldown=90, duration=2, name="War Stomp", icon="ability_warstomp.jpg")

################################################################################
# Gnome

# Instantly escape the effects of any movement impairing effect and gain immunity to those effects for 3 sec.
# OTHER_RACIALS.add_spell(spell_id=20589, cooldown=120, duration=3, name="Escape Artist", icon="ability_rogue_trip.jpg")

# Gnome
# Your non-periodic damaging abilities have their Energy cost reduced by 10% and deal 10% more damage for 8 sec.
OTHER_RACIALS.add_spell(spell_id=1259812, cooldown=120, duration=8, name="Eureka!", icon="inv_gnometoy.jpg", variations=[1259817, 1259823, 1259821, 1259813])


################################################################################
# Troll

# Increases your spellcasting and attack speed by 10% for 15 sec.
OTHER_RACIALS.add_spell(spell_id=20554, cooldown=180, duration=15, name="Berserking", icon="racial_troll_berserk.jpg")

# Regenerate 50% of your maximum Health over 6 sec. Any movement, action, or damage taken will cancel the
# effect.
# OTHER_RACIALS.add_spell(spell_id=1260270, cooldown=180, duration=6, name="Rapid Regeneration", icon="ability_racial_regeneratin.jpg")

################################################################################
# Skyborn

# Attempt to tap into the power of a nearby leyline, increasing your Health and Mana regeneration by 50% for 15
# sec. If a leyline is nearby, you will become Attuned for the next 1 hour and the effect of this ability will
# be increased by 100%.
OTHER_RACIALS.add_spell(spell_id=1259705, cooldown=120, duration=15, name="Read Leyline", icon="ability_mage_incantersabsorbtion.jpg")

# Glide downward through the air for 10 sec while controlling your direction of travel.
# OTHER_RACIALS.add_spell(spell_id=1259416, cooldown=90, duration=10, name="Walk on Air", icon="inv_elemental_primal_air.jpg")

# Race 96 (Forever)
# Attempt to draw power from a convergence of elements and receive its blessing, increasing your movement and
# mounted movement speeds by 15% for 30 sec. If an elemental convergence is nearby, you will become Charged for
# the next 1 hour and the effect of this ability will be increased by 100%.
# OTHER_RACIALS.add_spell(spell_id=1259686, cooldown=120, duration=30, name="Skysight", icon="ability_skyreach_lens_flare.jpg")


for spell in OTHER_RACIALS.spells:
    spell.show = False

for role in ALL_ROLES:
    for spec in role.specs:
        spec.add_spells(*OTHER_RACIALS.spells)
