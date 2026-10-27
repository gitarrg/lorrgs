"""Define the Mage Class and its Specs (WoW Forever)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.roles import RDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


################################################################################
# Class
#
MAGE = WowClass(id=8, name="Mage", color="#3FC7EB")

################################################################################
# Specs
#
MAGE_ARCANE = WowSpec(id=62, index=1, role=RDPS, wow_class=MAGE, name="Arcane")
MAGE_FIRE = WowSpec(id=63, index=2, role=RDPS, wow_class=MAGE, name="Fire")
MAGE_FROST = WowSpec(id=64, index=3, role=RDPS, wow_class=MAGE, name="Frost")
