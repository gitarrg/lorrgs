"""Entombed Sentinels (The Venomous Abyss)."""

from lorgs.data.classes import *
from lorgs.models import warcraftlogs_fight
from lorgs.models.raid_boss import RaidBoss


ENTOMBED_SENTINELS = RaidBoss(
    id=3445,
    name="Entombed Sentinels",
    nick="Sentinels",
    icon="inv_121_raid_achievement_golems.jpg",
    phase_type=RaidBoss.PhaseType.DYNAMIC,
)
boss = ENTOMBED_SENTINELS


# Timeline Reminder only tracks the "Phase 1" phases
# so we get rid of the other phases
# def filter_phases(fight: warcraftlogs_fight.Fight, status: str) -> None:
#     """Filter the phases for the boss."""
#     if status != "success":
#         return
#     if not fight.boss or (fight.boss.boss_slug != ENTOMBED_SENTINELS.name_slug):
#         return
# 
#     # remove any non p1 phases
#     fight.phases = [phase for phase in fight.phases if phase.phase_id == 1]
# 
#     # renumber the phases (start at 2, since p1=pull)
#     for i, phase in enumerate(fight.phases, start=2):
#         phase.phase_id = i
# 
# 
# warcraftlogs_fight.Fight.event_fight_load.connect(filter_phases)
# warcraftlogs_fight.Fight.event_fight_phases_load.connect(filter_phases)

boss.add_phase_info(transition_id=2, skip=True)


################################################################################
# Trinkets


################################################################################
# Spells


boss.add_cast(
    spell_id=1296878,
    name="Shifting Protovenom",
    duration=8,
    color="rgb(245, 158, 20)",
    icon="spell_deathvortex.jpg",
)


# Intermissions
boss.add_cast(
    spell_id=1284635,
    name="Vitriolic Stasis",
    duration=30,
    color="rgb(230, 41, 120)",
    icon="inv_112_raidtrinkets_blobofswirlingvoid_dark.jpg",
)


########################
# Blood of Ula'tek

# Tank
boss.add_cast(
    spell_id=1284487,
    name="Bloodvenom Injection",
    duration=1.5,
    color="rgb(217, 189, 178)",
    icon="ability_warrior_bloodbath.jpg",
    show=False,
)
boss.add_cast(
    spell_id=1288232,
    name="Unstable Miasma",
    duration=8,
    color="rgb(242, 68, 24)",
    icon="ability_deathwing_bloodcorruption_death.jpg",
    show=False,
)
boss.add_cast(
    spell_id=1284471,
    name="Blighted Blood",
    duration=8,
    color="rgb(128, 26, 13)",
    icon="spell_shadow_lifedrain.jpg",
)


########################
# Breath of Ula'tek

# tank hit
boss.add_cast(
    spell_id=1284458,
    name="Empowering Slam",
    duration=1.5,
    color="rgb(194, 166, 105)",
    icon="inv_mace_1h_pvppandarias3_c_01.jpg",
    show=False,
)
boss.add_cast(
    spell_id=1284434,
    name="Toxic Droplets",
    duration=16,
    color="rgb(164, 217, 80)",
    icon="inv_ability_poison_orb.jpg",
    show=False,
)
boss.add_cast(
    spell_id=1284251,
    name="Venom Coagulation",
    duration=1.5,
    color="rgb(68, 133, 16)",
    icon="inv_ability_poison_nova.jpg",
)
