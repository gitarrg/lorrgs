"""Nek'zali the Soulcoiler (The Venomous Abyss)."""

from lorgs.data.classes import *
from lorgs.models import warcraftlogs_actor, warcraftlogs_boss, warcraftlogs_fight
from lorgs.models.raid_boss import RaidBoss


NEKZALI = RaidBoss(
    id=3470,
    name="Nek'zali the Soulcoiler",
    nick="Nek'zali",
    icon="inv_121_raid_achievement_priestess.jpg",
    phase_type=RaidBoss.PhaseType.DYNAMIC,
)
boss = NEKZALI


# Timeline Reminder only tracks the "Phase 1" phases
# so we get rid of the other phases
def filter_phases(boss: warcraftlogs_actor.BaseActor, status: str) -> None:
    """Filter the phases for the boss."""
    if status != "success":
        return
    if not isinstance(boss, warcraftlogs_boss.Boss):
        return
    if not boss or (boss.boss_slug != NEKZALI.name_slug):
        return

    fight = boss.fight
    if not fight:
        return

    old_phases = fight.phases[:]
    fight.phases = []

    # Ritual of Awakening: Intermission 1.5
    if ritual_of_awakening_casts := [cast for cast in boss.casts if cast.spell_id == 1295124]:
        fight.add_phase(ts=ritual_of_awakening_casts[0].timestamp, phase_id=1.5)

    # Soul Transfer: Intermission 1.75
    if soul_transfer_casts := [cast for cast in boss.casts if cast.spell_id == 1292248]:
        fight.add_phase(
            # event is cast end. Phase start on cast start
            ts=soul_transfer_casts[-1].timestamp - 15_000,
            phase_id=1.75,
        )

    # Phase 2: Uncoiling buff applied
    phase_2 = old_phases[-1]
    fight.add_phase(ts=phase_2.timestamp, phase_id=2)


warcraftlogs_fight.Boss.event_actor_load.connect(filter_phases)


################################################################################
# Trinkets


################################################################################
# Spells


boss.add_cast(
    spell_id=1292248,
    name="Soul Transfer",
    duration=15,
    color="rgb(49, 97, 72)",
    icon="ability_necrolord_fleshcraft.jpg",
)


boss.add_cast(
    spell_id=1295124,
    name="Ritual of Awakening",
    duration=20,
    color="rgb(161, 91, 66)",
    icon="inv_helm_mail_raidshamanmythic_s_01.jpg",
)


boss.add_cast(
    spell_id=1285681,
    name="Soulcoil Ignition",
    duration=4,
    color="rgb(116, 213, 242)",
    icon="spell_shadow_soulleech_2.jpg",
)


boss.add_cast(
    spell_id=1299673,
    name="Invoke",
    duration=5,
    color="rgb(204, 179, 155)",
    icon="warrior_disruptingshout.jpg",
)


boss.add_cast(
    spell_id=1284103,
    name="Possession Barrage",
    duration=6,
    color="rgb(127, 47, 173)",
    icon="spell_shadow_possession.jpg",
    show=True,
)
