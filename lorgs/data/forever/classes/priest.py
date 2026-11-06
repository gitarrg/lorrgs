"""Define the Priest Class and its Specs (WoW Forever)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.forever.roles import HEAL, RDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


################################################################################
# Class
#
PRIEST = WowClass(id=5, name="Priest", color="#FFFFFF", talent_tree_id=1114)

################################################################################
# Specs
#
PRIEST_DISCIPLINE = WowSpec(id=256, index=1, role=HEAL, wow_class=PRIEST, name="Discipline", short_name="Disc")
PRIEST_HOLY = WowSpec(id=257, index=2, role=HEAL, wow_class=PRIEST, name="Holy")
PRIEST_SHADOW = WowSpec(id=258, index=3, role=RDPS, wow_class=PRIEST, name="Shadow")

################################################################################
# Spells
#
# Spellbook
# Chastise the target, causing 272 to 306 Holy damage and Immobilizing them for up to 2 sec. Only works against
# Humanoids. This spell causes very low threat.
# PRIEST.add_spell(spell_id=1277335, cooldown=120, duration=2, name="Chastise", icon="spell_holy_chastise.jpg")

# Confuses up to 5 enemies within 8 yds for 3 sec. Any damage taken will break the effect.
# PRIEST.add_spell(spell_id=1277455, cooldown=120, duration=3, name="Confounding Flash", icon="ability_paladin_blindinglight2.jpg")

# Place a Holy ward on an ally for 30 sec. The next time this ally takes damage dropping their Health below 35%,
# they will gain a shield absorbing 926 damage and begin healing for 670 Health over 15 sec. A target may be
# affected by only one Contingency Plan.
PRIEST.add_spell(spell_id=1277640, cooldown=600, duration=30, name="Contingency Plan", icon="ability_priest_soulwarding.jpg", show=False)

# Cannibalize 1640 of your own Health over 15 sec to gain (1640 + Spirit) Mana.
PRIEST.add_spell(spell_id=1277328, cooldown=600, duration=15, name="Dark Sacrifice", icon="spell_holy_powerinfusion_shadow.jpg")

# Instantly heals the caster for 1318 to 1546.
PRIEST.add_spell(spell_id=19243, cooldown=600, name="Desperate Prayer", icon="spell_holy_restoration.jpg", show=False)

# Instantly heals a friendly target below 50% Health for 1318 to 1546 and removes Weakened Soul from that
# target. Cannot be cast on self.
PRIEST.add_spell(spell_id=1277378, cooldown=600, name="Divine Grace", icon="ability_priest_savinggrace.jpg")

# Reduces the chance you'll be hit by melee and ranged attacks by 50% for 15 sec or until you are missed 3
# times.
PRIEST.add_spell(spell_id=2651, cooldown=300, duration=15, name="Elune's Grace", icon="spell_holy_elunesgrace.jpg", show=False)

# Wards the friendly target against Fear. The next Fear effect used against the target will fail, using up the
# ward. Lasts 3 min.
PRIEST.add_spell(spell_id=6346, cooldown=180, duration=180, name="Fear Ward", icon="spell_holy_excorcism.jpg")

# The priest becomes surrounded with anti-magic energy. Any successful spell cast against the priest will burn
# 105 of the attacker's Mana, causing 1 Shadow damage for each point of Mana burned. Lasts 15 sec.
PRIEST.add_spell(spell_id=19275, cooldown=180, duration=15, name="Feedback", icon="spell_shadow_ritualofsacrifice.jpg", show=False)

# Creates a holy Lightwell near the priest. Members of your raid or party can click the Lightwell to restore
# 1600 health over 10 sec. Being attacked cancels the effect. Lightwell lasts for 3 min or 5 charges.
PRIEST.add_spell(spell_id=27871, cooldown=600, duration=180, name="Lightwell", icon="spell_holy_summonlightwell.jpg")

# Talents: Discipline
# When activated, reduces the Mana cost of your next spell by 100% and increases its critical effect chance by
# 25% if it is a non-periodic spell and capable of a critical effect.
PRIEST_DISCIPLINE.add_spell(spell_id=14751, cooldown=180, name="Inner Focus", icon="spell_frost_windwalkon.jpg")
# Infuses the target with power, increasing their spell damage and healing done by 20% for 15 sec.
PRIEST_DISCIPLINE.add_spell(spell_id=10060, cooldown=180, duration=15, name="Power Infusion", icon="spell_holy_powerinfusion.jpg")
