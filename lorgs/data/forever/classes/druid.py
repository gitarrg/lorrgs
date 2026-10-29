"""Define the Druid Class and its Specs (WoW Forever)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.forever.roles import HEAL, MDPS, RDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


################################################################################
# Class
#
DRUID = WowClass(id=11, name="Druid", color="#FF7C0A")

################################################################################
# Specs
#
DRUID_BALANCE = WowSpec(id=102, index=1, role=RDPS, wow_class=DRUID, name="Balance")
DRUID_FERAL = WowSpec(id=103, index=2, role=MDPS, wow_class=DRUID, name="Feral")
DRUID_RESTORATION = WowSpec(id=105, index=3, role=HEAL, wow_class=DRUID, name="Restoration", short_name="Resto")
