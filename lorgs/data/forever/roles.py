"""The Roles of the forever Game Version."""

from lorgs.models.wow_role import WowRole


################################################################################
# ROLES
#
TANK = WowRole(id=1, code="tank", name="Tank")
HEAL = WowRole(id=2, code="heal", name="Healer", metric="hps")
MDPS = WowRole(id=3, code="mdps", name="Melee", metrics=["dps", "bossdps"])
RDPS = WowRole(id=4, code="rdps", name="Range", metrics=["dps", "bossdps"])
MIXED = WowRole(id=2001, code="mix", name="Mixed")

ALL_ROLES = [TANK, HEAL, MDPS, RDPS]
