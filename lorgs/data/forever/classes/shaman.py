"""Define the Shaman Class and its Specs (WoW Forever)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.roles import HEAL, MDPS, RDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


################################################################################
# Class
#
SHAMAN = WowClass(id=7, name="Shaman", color="#0070DD")

################################################################################
# Specs
#
SHAMAN_ELEMENTAL = WowSpec(id=262, index=1, role=RDPS, wow_class=SHAMAN, name="Elemental")
SHAMAN_ENHANCEMENT = WowSpec(id=263, index=2, role=MDPS, wow_class=SHAMAN, name="Enhancement")
SHAMAN_RESTORATION = WowSpec(id=264, index=3, role=HEAL, wow_class=SHAMAN, name="Restoration", short_name="Resto")
