"""Shared logic for loading Fights.

Create "FightPlans" and pass them to `load_fight` or `load_fights`.

"""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import asyncio
import dataclasses
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.loaders.boss_loader import BossLoader
from lorgs.loaders.fight_loader import FightLoader
from lorgs.loaders.fight_phases import FightPhasesLoader
from lorgs.loaders.player_loader import PlayerLoader
from lorgs.logger import logger


if typing.TYPE_CHECKING:
    from lorgs.clients.wcl.client import WarcraftlogsClient
    from lorgs.loaders.base_loader import BaseLoader
    from lorgs.models.game_data import GameData
    from lorgs.models.warcraftlogs_fight import Fight


@dataclasses.dataclass
class FightPlan:
    """What to load for one Fight."""

    fight: Fight
    """The Fight to load."""

    players: typing.Literal["all"] | list[int] | None = None
    """The players to load.

    - "all": All players
    - list[int]: The source ids of the players to load
    - None: No players
    """

    boss: bool = False
    """Whether to load the boss."""


@dataclasses.dataclass
class FightFailure:
    """A Fight that could not be loaded, and why."""

    fight: Fight
    error: Exception


async def load_fight(
    plan: FightPlan,
    game_data: GameData,
    client: WarcraftlogsClient | None,
) -> FightFailure | None:
    """Load a single Fight.

    Args:
        plan: The FightPlan to load.
        game_data: The GameData to use.
        client: The WarcraftlogsClient to use.

    Returns:
        A FightFailure if the Fight failed to load, otherwise None.

    """
    try:
        await _load_steps(plan, game_data, client)
    except Exception as error:  # ruff: ignore[blind-except]  # one Fight must not fail the others
        logger.exception("Failed to load fight %s", plan.fight.fight_id)
        return FightFailure(fight=plan.fight, error=error)
    return None


async def load_fights(
    plans: list[FightPlan],
    game_data: GameData,
    client: WarcraftlogsClient | None = None,
) -> list[FightFailure]:
    """Load every planned Fight concurrently. Anything already loaded is skipped.

    Args:
        plans: The FightPlans to load.
        game_data: The GameData to use.
        client: The WarcraftlogsClient to use.

    Returns:
        A list of FightFailures, one for each Fight that failed to load.

    """
    results = await asyncio.gather(*[load_fight(plan, game_data, client) for plan in plans])
    return [failure for failure in results if failure]


async def _load_steps(
    plan: FightPlan,
    game_data: GameData,
    client: WarcraftlogsClient | None,
) -> None:
    fight = plan.fight

    # 1. Fight summary (players, Composition). Also fills the Phases when the boss needs no Casts for them.
    summary_loader = FightLoader(fight, game_data)
    if summary_loader.needs_load():
        await summary_loader.load(client=client)

    # 2. Phases. `RaidBoss.process_phases` runs here, on the Casts the Phase query fetches itself.
    phases_loader = FightPhasesLoader(fight, game_data)
    if phases_loader.needs_load():
        await phases_loader.load(client=client)

    # 3. Actors
    loaders: list[BaseLoader] = []
    if plan.boss and fight.boss:
        loaders.append(BossLoader(fight.boss, game_data))
    for player in fight.players:
        if plan.players == "all" or (plan.players and player.source_id in plan.players):
            loaders.append(PlayerLoader(player, game_data=game_data))

    loaders = [loader for loader in loaders if loader.needs_load()]
    if loaders:
        await asyncio.gather(*[loader.load(client=client) for loader in loaders])
