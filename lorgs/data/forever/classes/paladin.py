"""Define the Paladin Class and its Specs (WoW Forever)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.forever.roles import HEAL, MDPS, TANK
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


################################################################################
# Class
#
PALADIN = WowClass(id=2, name="Paladin", color="#F48CBA")

################################################################################
# Specs
#
PALADIN_HOLY = WowSpec(id=65, index=1, role=HEAL, wow_class=PALADIN, name="Holy")
PALADIN_PROTECTION = WowSpec(id=66, index=2, role=TANK, wow_class=PALADIN, name="Protection", short_name="Prot")
PALADIN_RETRIBUTION = WowSpec(id=70, index=3, role=MDPS, wow_class=PALADIN, name="Retribution", short_name="Ret")
