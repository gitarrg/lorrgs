"""Define the Rogue Class and its Specs (WoW Forever)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.roles import MDPS
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


################################################################################
# Class
#
ROGUE = WowClass(id=4, name="Rogue", color="#FFF468")

################################################################################
# Specs
#
ROGUE_ASSASSINATION = WowSpec(id=259, index=1, role=MDPS, wow_class=ROGUE, name="Assassination", short_name="Assa")
ROGUE_COMBAT = WowSpec(id=260, index=2, role=MDPS, wow_class=ROGUE, name="Combat")
ROGUE_SUBTLETY = WowSpec(id=261, index=3, role=MDPS, wow_class=ROGUE, name="Subtlety")
