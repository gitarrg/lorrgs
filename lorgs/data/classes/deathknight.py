"""Define the Death Knight Class and all its Specs and Spells."""

# pylint: disable=line-too-long
# pylint: disable=bad-whitespace
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.constants import *
from lorgs.data.roles import *
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag, WowSpell


################################################################################
# Class
#
DEATHKNIGHT = WowClass(id=6, name="Death Knight", color="#C41E3A")

################################################################################
# Specs
#
DEATHKNIGHT_BLOOD  = WowSpec(id=250, index=1, role=TANK, wow_class=DEATHKNIGHT, name="Blood")
DEATHKNIGHT_FROST  = WowSpec(id=251, index=2, role=MDPS, wow_class=DEATHKNIGHT, name="Frost")
DEATHKNIGHT_UNHOLY = WowSpec(id=252, index=3, role=MDPS, wow_class=DEATHKNIGHT, name="Unholy")

################################################################################
# Spells
#

# Utility
DEATHKNIGHT.add_spell(         spell_id=48265,  cooldown=45,  duration=10, color="#b82cbf", name="Death's Advance",       icon="spell_shadow_demonicempathy.jpg",           show=False, tags=[SpellTag.MOVE], variations=[444347])

# Defensive
DEATHKNIGHT.add_spell(         spell_id=51052,  cooldown=120, duration=10, color="#d58cff", name="Anti-Magic Zone",       icon="spell_deathknight_antimagiczone.jpg",      show=False, tags=[SpellTag.RAID_CD])
DEATHKNIGHT.add_spell(         spell_id=48707,  cooldown=60,  duration=5,  color="#8ced53", name="Anti-Magic Shell",      icon="spell_shadow_antimagicshell.jpg",          show=False)
DEATHKNIGHT.add_spell(         spell_id=48792,  cooldown=180, duration=8,  color="#53aaed", name="Icebound Fortitude",    icon="spell_deathknight_iceboundfortitude.jpg", tags=[SpellTag.DEFENSIVE])
DEATHKNIGHT.add_spell(         spell_id=49039,  cooldown=120, duration=10, color="#999999", name="Lichborne",             icon="spell_shadow_raisedead.jpg")

# Hero Talents
DEATHKNIGHT.add_spell(         spell_id=439843, cooldown=45,  duration=12, color="#1ce6d5", name="Reaper's Mark",         icon="inv_ability_deathbringerdeathknight_reapersmark.jpg", show=False)


# Offensive
DEATHKNIGHT_BLOOD.add_spell(   spell_id=49028,  cooldown=120, duration=8,  color="#ffbd24", name="Dancing Rune Weapon",   icon="inv_sword_07.jpg", tags=[SpellTag.TANK])
DEATHKNIGHT_BLOOD.add_spell(   spell_id=55233,  cooldown=90,  duration=10,                  name="Vampiric Blood",        icon="spell_shadow_lifedrain.jpg", tags=[SpellTag.TANK])
DEATHKNIGHT_BLOOD.add_debuff(  spell_id=123981, cooldown=240, duration=3,  color="#31b038", name="Purgatory",             icon="inv_misc_shadowegg.jpg",                  show=False, tags=[SpellTag.TANK])

DEATHKNIGHT_UNHOLY.add_spell(  spell_id=42650,  cooldown=240, duration=30,                  name="Army of the Dead",      icon="spell_deathknight_armyofthedead.jpg",                 tags=[SpellTag.DYNAMIC_CD, SpellTag.DAMAGE])
DEATHKNIGHT_UNHOLY.add_spell(  spell_id=1233448,  cooldown=45,  duration=15,                  name="Dark Transformation",   icon="achievement_boss_festergutrotface.jpg",               tags=[SpellTag.DYNAMIC_CD, SpellTag.DAMAGE])

DEATHKNIGHT_FROST.add_spell(   spell_id=51271,  cooldown=60,  duration=12,                  name="Pillar of Frost",       icon="ability_deathknight_pillaroffrost.jpg",    show=False)
DEATHKNIGHT_FROST.add_spell(   spell_id=46585,  cooldown=120, duration=60, color="#c7ba28", name="Raise Dead",            icon="inv_pet_ghoul.jpg",                        show=False)
DEATHKNIGHT_FROST.add_buff(    spell_id=1249658,cooldown=90,            color="#52abff", name="Breath of Sindragosa",  icon="spell_deathknight_breathofsindragosa.jpg", tags=[SpellTag.DAMAGE])
DEATHKNIGHT_FROST.add_spell(   spell_id=279302, cooldown=90,                               name="Frostwyrm's Fury",      icon="achievement_boss_sindragosa.jpg", tags=[SpellTag.DAMAGE])

# Additional Spells (not tracked)
RAISE_ALLY = WowSpell(spell_id=61999, name="Raise Ally", icon="spell_shadow_deadofnight.jpg")
