"""0:


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/AvbNVBmyrKPDCT4L?fight=13"

"""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.wow_trinket import WowTrinket


LOOMITHAR = RaidBoss(
    id=3131,
    name="Loom'ithar",
    nick="Loom'ithar",
    icon="inv_112_achievement_raid_silkworm.jpg",
)
boss = LOOMITHAR


################################################################################
# Trinkets

LOOMITHARS_LIVING_SILK = WowTrinket(
    spell_id=1232721,
    cooldown=90,
    duration=10,
    name="Loom'ithar's Living Silk",
    icon="inv_112_raidtrinkets_astralspinneret.jpg",
    item=242393,
)
"""Shield on target

> Use: Weave an arcane cocoon around yourself and four nearby allies for 10 sec,
> reducing their damage taken by 75% until 3001672 damage has been prevented.
> 
> If a cocoon expires, it bursts to heal an injured ally for 50% of its remaining power.
> (1 Min, 30 Sec Cooldown)

"""
LOOMITHARS_LIVING_SILK.add_specs(*HEAL.specs)


################################################################################
# Phase 1


# Tank: Beam
boss.add_cast(
    spell_id=1227261,
    name="Piercing Strand",
    duration=3,
    cooldown=45,
    # color="hsl(30, 60%, 50%)",
    icon="inv_112_arcane_beam.jpg",
    show=False,
)


boss.add_cast(
    spell_id=1237272,
    name="Lair Weaving",
    duration=5,
    # cooldown=45,
    # color="hsl(30, 60%, 50%)",
    icon="inv_ability_web_buff.jpg",
)


# TODO:
# Soak beams = "Hyper Infusion"
# Webs = "Infusion Tether"


################################################################################
# Phase 2


# Frontal
boss.add_cast(
    spell_id=1227226,
    name="Writhing Wave",
    duration=4,
    cooldown=25,
    color="hsl(30, 60%, 50%)",
    icon="inv_ability_web_wave.jpg",
)

# Spread
boss.add_cast(
    spell_id=1227782,
    name="Arcane Outrage",
    duration=2,
    cooldown=4,
    color="hsl(10, 60%, 50%)",
    icon="inv_112_raidsilkworm_arcaneoutrage.jpg",
)


################################################################################
# Phases
boss.add_phase(name="P2", spell_id=1228070, event_type="applybuff", count=1)  # Unbound Rage
