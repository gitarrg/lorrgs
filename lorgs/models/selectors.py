"""Turn selectors (spec, boss, difficulty, metric) into the Spec Rankings they name.

API routes, SQS handlers and scripts all pick Spec Rankings the same way:
- spec: a slug, or `all` for every playable spec (no item pseudo-specs).
- boss: a slug, or `all` for every boss of the current season.
- difficulty: a name, `auto` for the one we rank per raid, or `all` for every difficulty we rank per raid.
- metric: a name, empty for the spec's role default, or `all` for every metric of the spec's role.
"""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import dataclasses
import typing


if typing.TYPE_CHECKING:
    from collections.abc import Iterable

    from lorgs.models.game_data import GameData
    from lorgs.models.raid_boss import RaidBoss
    from lorgs.models.wow_spec import WowSpec


ALL = "all"
"""Selector value for every spec, boss, difficulty or metric."""

DEFAULT_METRIC = "dps"
"""Metric for an unknown spec."""


@dataclasses.dataclass(frozen=True)
class SpecRankingKey:
    """The selectors of one Spec Ranking, with every token resolved."""

    spec: WowSpec
    boss: RaidBoss
    difficulty: str
    metric: str


def playable_specs(game_data: GameData) -> list[WowSpec]:
    """The specs a player can be. Skips the pseudo-specs of non-playable roles (eg.: other-trinkets)."""
    return [spec for spec in game_data.specs if spec.role.playable]


def select_specs(game_data: GameData, spec_slug: str) -> list[WowSpec]:
    """`all` is every playable spec. An unknown slug selects nothing."""
    if spec_slug == ALL:
        return playable_specs(game_data)
    spec = game_data.get_spec(spec_slug)
    return [spec] if spec else []


def select_bosses(game_data: GameData, boss_slug: str) -> list[RaidBoss]:
    """`all` is every boss of the current season. An unknown slug selects nothing."""
    if boss_slug == ALL:
        return list(game_data.bosses)
    boss = game_data.get_boss(full_name_slug=boss_slug)
    return [boss] if boss else []


def select_difficulties(game_data: GameData, boss_slug: str, difficulty: str) -> list[str]:
    """`all` is every difficulty we rank for the boss, `auto` the one of its zone."""
    if difficulty == ALL:
        return game_data.difficulties_for_boss(boss_slug)
    return [game_data.resolve_difficulty(boss_slug, difficulty)]


def default_metric(spec: WowSpec | None) -> str:
    """The metric a spec is ranked by unless asked otherwise. eg.: hps for healers."""
    return spec.role.metric if spec else DEFAULT_METRIC


def select_metrics(spec: WowSpec | None, metric: str) -> list[str]:
    """`all` is every metric of the spec's role. Empty is the role's default."""
    if metric == ALL:
        return list(spec.role.metrics) if spec else [DEFAULT_METRIC]
    return [metric or default_metric(spec)]


def expand_selectors(
    game_data: GameData,
    specs: Iterable[WowSpec],
    bosses: Iterable[RaidBoss],
    difficulty: str,
    metric: str,
) -> list[SpecRankingKey]:
    """Every Spec Ranking of these specs and bosses, with `difficulty` and `metric` resolved per boss and spec."""
    bosses = list(bosses)
    return [
        SpecRankingKey(spec, boss, boss_difficulty, spec_metric)
        for spec in specs
        for boss in bosses
        for boss_difficulty in select_difficulties(game_data, boss.full_name_slug, difficulty)
        for spec_metric in select_metrics(spec, metric)
    ]
