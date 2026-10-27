"""Define the Death Knight Class and its Specs (MoP Classic)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.roles import MDPS, TANK
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag


################################################################################
# Class
#
DEATHKNIGHT = WowClass(id=6, name="Death Knight", color="#C41E3A")

################################################################################
# Specs
#
DEATHKNIGHT_BLOOD = WowSpec(id=250, index=1, role=TANK, wow_class=DEATHKNIGHT, name="Blood")
DEATHKNIGHT_FROST = WowSpec(id=251, index=2, role=MDPS, wow_class=DEATHKNIGHT, name="Frost")
DEATHKNIGHT_UNHOLY = WowSpec(id=252, index=3, role=MDPS, wow_class=DEATHKNIGHT, name="Unholy")

################################################################################
# Spells
#
DEATHKNIGHT.add_spell(spell_id=48792,  cooldown=180, duration=12, name="Icebound Fortitude",              icon="spell_deathknight_iceboundfortitude.jpg", show=False, tags=[SpellTag.DEFENSIVE])
DEATHKNIGHT.add_spell(spell_id=49039,  cooldown=120, duration=10, name="Lichborne",                       icon="spell_shadow_raisedead.jpg", show=False, tags=[SpellTag.DEFENSIVE])
DEATHKNIGHT.add_spell(spell_id=47568,  cooldown=300,              name="Empower Rune Weapon",             icon="inv_sword_62.jpg", show=False)
DEATHKNIGHT.add_spell(spell_id=42650,  cooldown=600, duration=40, name="Army of the Dead",                icon="spell_deathknight_armyofthedead.jpg", show=False, tags=[SpellTag.DAMAGE])

DEATHKNIGHT_BLOOD.add_spell(spell_id=55233,  cooldown=60,  duration=10, name="Vampiric Blood",                  icon="spell_shadow_lifedrain.jpg", tags=[SpellTag.TANK])
DEATHKNIGHT_BLOOD.add_spell(spell_id=49028,  cooldown=90,  duration=12, name="Dancing Rune Weapon",             icon="inv_sword_07.jpg", tags=[SpellTag.TANK])

DEATHKNIGHT_FROST.add_spell(spell_id=51271,  cooldown=60,  duration=20, name="Pillar of Frost",                 icon="ability_deathknight_pillaroffrost.jpg", tags=[SpellTag.DAMAGE])

DEATHKNIGHT_UNHOLY.add_spell(spell_id=49206,  cooldown=180, duration=30, name="Summon Gargoyle",                 icon="ability_deathknight_summongargoyle.jpg", tags=[SpellTag.DAMAGE])
