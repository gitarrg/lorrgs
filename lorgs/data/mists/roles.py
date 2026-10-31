"""The Roles of the mists Game Version. Deliberately a copy of the other Game Versions' roles."""

from lorgs.models.wow_role import WowRole


################################################################################
# ROLES
#
TANK = WowRole(id=1, code="tank", name="Tank")
HEAL = WowRole(id=2, code="heal", name="Healer", metric="hps")
MDPS = WowRole(id=3, code="mdps", name="Melee", metrics=["dps", "bossdps"])
RDPS = WowRole(id=4, code="rdps", name="Range", metrics=["dps", "bossdps"])

ALL_ROLES = [TANK, HEAL, MDPS, RDPS]
