"""0:


>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/AvbNVBmyrKPDCT4L?fight=13"

"""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss


LOOMITHAR = RaidBoss(
    id=3131,
    name="Loom'ithar",
    nick="Loom'ithar",
    icon="inv_112_achievement_raid_silkworm.jpg",
)
boss = LOOMITHAR


################################################################################
# Trinkets

LOOMITHARS_LIVING_SILK = boss.add_trinket(
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


boss.add_cast(
    spell_id=1226395,
    name="Overinfusion Burst",
    duration=8,
    color="rgb(247, 40, 78)",
    icon="spell_nature_wispsplode.jpg",
)


# Unable to find a matching cast/event to track this
# boss.add_cast(
#     spell_id=1250103,
#     name="Infusion Pylons",
#     duration=19,
#     color="rgb(240, 62, 186)",
#     icon="spell_mage_overpowered.jpg",
# )


boss.add_cast(
    spell_id=1237272,
    name="Lair Weaving",
    duration=5,
    color="rgb(200, 230, 226)",
    icon="inv_ability_web_buff.jpg",
)


# boss.add_cast(
#     spell_id=1226311,
#     name="Infusion Tether",
#     duration=5,
#     color="rgb(240, 159, 72)",
#     icon="inv_ability_web_beam.jpg",
# )


# Tank: Beam
boss.add_cast(
    spell_id=1227263,
    name="Piercing Strand",
    color="rgb(95, 103, 245)",
    duration=3,
    cooldown=45,
    icon="inv_112_arcane_beam.jpg",
    show=False,
    # spell id might be 1227261?
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
    color="rgb(100, 237, 182)",
    icon="inv_ability_web_wave.jpg",
)

# Spread
boss.add_cast(
    spell_id=1227782,
    name="Arcane Outrage",
    duration=2,
    cooldown=4,
    color="rgb(169, 64, 230)",
    icon="inv_112_raidsilkworm_arcaneoutrage.jpg",
)


################################################################################
# Phases
boss.add_phase(name="P2", spell_id=1228070, event_type="applybuff", count=1)  # Unbound Rage
