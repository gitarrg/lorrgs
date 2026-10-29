"""Define the Priest Class and its Specs (WoW Forever)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.forever.roles import HEAL, RDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


################################################################################
# Class
#
PRIEST = WowClass(id=5, name="Priest", color="#FFFFFF")

################################################################################
# Specs
#
PRIEST_DISCIPLINE = WowSpec(id=256, index=1, role=HEAL, wow_class=PRIEST, name="Discipline", short_name="Disc")
PRIEST_HOLY = WowSpec(id=257, index=2, role=HEAL, wow_class=PRIEST, name="Holy")
PRIEST_SHADOW = WowSpec(id=258, index=3, role=RDPS, wow_class=PRIEST, name="Shadow")
