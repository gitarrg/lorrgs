"""RaidZone and Bosses for Patch 10.0 T31: Vault of the Incarnates, first raid tier of Dragonflight."""

# IMPORT LOCAL LIBRARIES
from lorgs.models.raid_zone import RaidZone

from .broodkeeper_diurna import DIURNA
from .dathea import DATHEA
from .eranog import ERANOG
from .kurog import KUROG
from .primal_council import PRIMAL_COUNCIL
from .raszageth import RASZAGETH
from .sennarth import SENNARTH
from .terros import TERROS


################################################################################
#
#   Tier: 31 Vault of the Incarnates
#
################################################################################
VAULT_OF_THE_INCARNATES = RaidZone(
    id=31,
    name="Vault of the Incarnates",
    icon="achievement_raidprimalist_raid.jpg",
    bosses=[
        ERANOG,
        TERROS,
        PRIMAL_COUNCIL,
        SENNARTH,
        DATHEA,
        KUROG,
        DIURNA,
        RASZAGETH,
    ],
)
