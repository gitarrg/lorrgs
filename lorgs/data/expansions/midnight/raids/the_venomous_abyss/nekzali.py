"""Nek'zali the Soulcoiler (The Venomous Abyss)."""

from typing import override

from lorgs.data.retail.classes import *
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.warcraftlogs_cast import Cast
from lorgs.models.warcraftlogs_fight import Phase


# WCL phase 3 is the Uncoiling buff. Earlier transitions are not Phase 2.
RITUAL_OF_AWAKENING = 1295124
SOUL_TRANSFER = 1292248
UNCOILING_TRANSITION = 3


class Nekzali(RaidBoss):
    id: int = 3470
    name: str = "Nek'zali the Soulcoiler"
    nick: str = "Nek'zali"
    icon: str = "inv_121_raid_achievement_priestess.jpg"
    phase_type: RaidBoss.PhaseType = RaidBoss.PhaseType.DYNAMIC
    phase_spells: list[int] = [
        RITUAL_OF_AWAKENING,
        SOUL_TRANSFER,
    ]

    @override
    def process_phases(self, phases: list[Phase], casts: list[Cast]) -> list[Phase]:
        """Rebuild Phases from the intermission Casts and the Uncoiling transition."""
        corrected = [Phase(ts=0, phase_id=1)]

        ritual_casts = [cast for cast in casts if cast.spell_id == RITUAL_OF_AWAKENING]
        if ritual_casts:
            corrected.append(Phase(ts=ritual_casts[0].timestamp, phase_id=1.5))

        soul_transfer_casts = [cast for cast in casts if cast.spell_id == SOUL_TRANSFER]
        if soul_transfer_casts:
            # This Cast is the end of Soul Transfer. The intermission starts when the cast starts.
            soul_transfer = next(spell for spell in self.spells if spell.spell_id == SOUL_TRANSFER)
            cast_start = soul_transfer_casts[-1].timestamp - int(soul_transfer.duration * 1000)
            corrected.append(Phase(ts=cast_start, phase_id=1.75))

        uncoiling = [phase for phase in phases if phase.phase_id == UNCOILING_TRANSITION]
        if uncoiling:
            corrected.append(Phase(ts=uncoiling[-1].timestamp, phase_id=2))

        return corrected


NEKZALI = Nekzali()
boss = NEKZALI


################################################################################
# Trinkets

SOULCOILER_RITUAL_VESSEL = boss.add_trinket(
    spell_id=1291894,
    duration=20,
    cooldown=120,
    name="Soulcoiler Ritual Vessel",
    icon="inv_121_trinket_raid_ulatek_ritualvessel.jpg",
    item=270162,
)
SOULCOILER_RITUAL_VESSEL.add_specs(*HEAL.specs)
"""On-Use ally barriers (channel)

> Use: Call forth 5 Soulcoiler Cultist spirits over 2 sec and sacrifice their
> essence, each granting an ally a barrier reducing damage taken by 50% for 20 sec
> or until the shield is consumed.
>
> Allied deaths reduce this cooldown by 30 sec and immediately summon a Soulcoil
> Cultist spirit for sacrifice. (2 Min Cooldown)
"""


################################################################################
# Spells


boss.add_cast(
    spell_id=SOUL_TRANSFER,
    name="Soul Transfer",
    duration=15,
    color="rgb(49, 97, 72)",
    icon="ability_necrolord_fleshcraft.jpg",
)


boss.add_cast(
    spell_id=RITUAL_OF_AWAKENING,
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
