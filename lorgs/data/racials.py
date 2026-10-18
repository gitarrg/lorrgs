"""Relevant Racials.

Ref: https://www.wowhead.com/spells/racial-traits
"""

# pylint: disable=line-too-long
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# fmt: off
from lorgs.data.classes import *
from lorgs.models.wow_spell import SpellType


# for now, lets just use the Trinket Type
SPELL_TYPE = SpellType.TRINKET

RACIALS = WowClass(id=1003, name="Racials")  # dummy container


################################################################################
# NEUTRAL
#
# Pandaren
# https://www.wowhead.com/spell=107079/quaking-palm (is that the Pandaren Racial?)


################################################################################
# FOR THE ALLIANCE!
#

# Draenei
# https://www.wowhead.com/spell=28880/gift-of-the-naaru

# Dwarf
RACIALS.add_buff(spell_type=SPELL_TYPE, spell_id=65116, cooldown=120, duration=8, color="#dba85c", name="Stoneform", icon="spell_shadow_unholystrength.jpg")

# Gnome
# https://www.wowhead.com/spell=20589/escape-artist

# Human
# https://www.wowhead.com/spell=59752/will-to-survive

# Night Elf
# https://www.wowhead.com/spell=58984/shadowmeld

# Worgen
# https://www.wowhead.com/spell=68992/darkflight

### Allied Races ###

# Void Elf
# https://www.wowhead.com/spell=256948/spatial-rift

# Lightforged Draenei
# _BASE.add_spell(spell_type=SPELL_TYPE, spell_id=255647, cooldown=150, duration=3, name="Light's Judgment", icon="ability_racial_orbitalstrike.jpg")

# Dark Iron Dwarf
RACIALS.add_buff(spell_type=SPELL_TYPE, spell_id=273104, cooldown=120, duration=8, color="#e03019", name="Fireblood", icon="ability_racial_fireblood.jpg")

# Kul Tiran
# https://www.wowhead.com/spell=287712/haymaker

# Mechagnome
# https://www.wowhead.com/spell=312924/hyper-organic-light-originator


################################################################################
# HORDE (also ok)
#

# Orc
RACIALS.add_spell(spell_type=SPELL_TYPE, spell_id=20572, cooldown=120, duration=15, color="#97bf52", name="Blood Fury", icon="racial_orc_berserkerstrength.jpg", variation=[33697, 33702])

# Undead
# https://www.wowhead.com/spell=20577/cannibalize
# https://www.wowhead.com/spell=7744/will-of-the-forsaken

# Tauren
# https://www.wowhead.com/spell=20549/war-stomp

# Troll
RACIALS.add_spell(spell_type=SPELL_TYPE, spell_id=26297, cooldown=180, duration=12, color="#d49e5d", name="Berserking", icon="racial_troll_berserk.jpg")

# Blood Elf
# https://www.wowhead.com/spell=28730/arcane-torrent

# Goblin
# https://www.wowhead.com/spell=20589/escape-artist

# Pandaren

### Allied Races ###

# Nightborne
# https://www.wowhead.com/spell=260364/arcane-pulse

# Highmountain Tauren
# https://www.wowhead.com/spell=255654/bull-rush

# Mag'har Orc
# WowSpell(spell_type=SPELL_TYPE, spell_id=274738, cooldown=120, duration=15, name="Ancestral Call", icon="ability_racial_ancestralcall.jpg"),

# Zandalari Troll
## WowSpell(spell_type=SPELL_TYPE, spell_id=262149, cooldown=120, duration=10, name="Regeneration", icon="ability_racial_regeneratin.jpg"),

# Vulpera
# https://www.wowhead.com/spell=312411/bag-of-tricks


for spell in (RACIALS.spells + RACIALS.buffs):
    spell.show = False


for s in ALL_SPECS:
    s.add_spells(*RACIALS.spells)
    s.add_buffs(*RACIALS.buffs)
