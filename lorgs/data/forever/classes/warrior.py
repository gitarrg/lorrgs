"""Define the Warrior Class and its Specs (WoW Forever)."""

# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.forever.roles import MDPS, TANK
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec


################################################################################
# Class
#
WARRIOR = WowClass(id=1, name="Warrior", color="#C69B6D")

################################################################################
# Specs
#
WARRIOR_ARMS = WowSpec(id=71, index=1, role=MDPS, wow_class=WARRIOR, name="Arms")
WARRIOR_FURY = WowSpec(id=72, index=2, role=MDPS, wow_class=WARRIOR, name="Fury")
WARRIOR_PROTECTION = WowSpec(id=73, index=3, role=TANK, wow_class=WARRIOR, name="Protection", short_name="Prot")
