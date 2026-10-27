"""Define the Hunter Class and its Specs (WoW Forever)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.roles import RDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


################################################################################
# Class
#
HUNTER = WowClass(id=3, name="Hunter", color="#AAD372")

################################################################################
# Specs
#
HUNTER_BEASTMASTERY = WowSpec(id=253, index=1, role=RDPS, wow_class=HUNTER, name="Beast Mastery")
HUNTER_MARKSMANSHIP = WowSpec(id=254, index=2, role=RDPS, wow_class=HUNTER, name="Marksmanship")
HUNTER_SURVIVAL = WowSpec(id=255, index=3, role=RDPS, wow_class=HUNTER, name="Survival")
