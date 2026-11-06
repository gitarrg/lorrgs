"""Buffs from other Specs (WoW Forever)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.forever.classes import DRUID
from lorgs.data.forever.classes.other import OTHER_EXTERNALS
from lorgs.data.forever.roles import HEAL


################################################################################
# Healer Only
#
# Increases the target's Mana regeneration by 400% and allows 100% of the target's Mana regeneration to continue
# while casting. Lasts 20 sec.
INNERVATE = OTHER_EXTERNALS.add_buff(color=DRUID.color, spell_id=29166, cooldown=360, duration=20, name="Innervate", icon="spell_nature_lightning.jpg")
for s in HEAL.specs:
    s.add_buffs(INNERVATE)


################################################################################

for spell in (OTHER_EXTERNALS.spells + OTHER_EXTERNALS.buffs + OTHER_EXTERNALS.debuffs):
    spell.show = False
