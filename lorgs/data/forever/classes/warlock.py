"""Define the Warlock Class and its Specs (WoW Forever)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.forever.roles import RDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


################################################################################
# Class
#
WARLOCK = WowClass(id=9, name="Warlock", color="#8788EE")

################################################################################
# Specs
#
WARLOCK_AFFLICTION = WowSpec(id=265, index=1, role=RDPS, wow_class=WARLOCK, name="Affliction", short_name="Aff")
WARLOCK_DEMONOLOGY = WowSpec(id=266, index=2, role=RDPS, wow_class=WARLOCK, name="Demonology", short_name="Demo")
WARLOCK_DESTRUCTION = WowSpec(id=267, index=3, role=RDPS, wow_class=WARLOCK, name="Destruction", short_name="Destro")
