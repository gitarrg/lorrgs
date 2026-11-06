"""Special Utility Role/Class/Spec for spells that don't belong to one class, such as racials (WoW Forever)."""

# IMPORT LOCAL LIBRARIES
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_role import WowRole
from lorgs.models.wow_spec import WowSpec


################################################################################
# Role
#
ITEM_ROLE = WowRole(id=1001, code="item", name="Items", playable=False)

################################################################################
# Class
#
OTHER = WowClass(id=1001, name="Other", color="#cccccc")

################################################################################
# "Specs"
#
OTHER_EXTERNALS = WowSpec(role=ITEM_ROLE, wow_class=OTHER, name="Externals")
OTHER_RACIALS = WowSpec(role=ITEM_ROLE, wow_class=OTHER, name="Racials")
