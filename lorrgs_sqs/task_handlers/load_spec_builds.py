"""Handler to work out the Builds of a spec."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.data import talent_trees
from lorgs.logger import logger
from lorgs.models import selectors, spec_builds, warcraftlogs_ranking
from lorgs.models.task_payloads import SpecBuildsPayload
from lorrgs_sqs.exceptions import TaskValidationError


if typing.TYPE_CHECKING:
    from lorgs.models.game_version import GameVersion
    from lorgs.models.wow_spec import WowSpec


def collect_pool(game_version: GameVersion, spec: WowSpec) -> list[dict[int, int]]:
    """The Talents of every player in every stored Spec Ranking of the spec in the current season.

    Only the spec's default metric: a Fight in the rankings of two metrics would count twice.
    """
    data = game_version.data
    keys = selectors.expand_selectors(data, [spec], selectors.select_bosses(data, selectors.ALL), selectors.ALL, "")

    pool: list[dict[int, int]] = []
    for key in keys:
        ranking = warcraftlogs_ranking.SpecRanking.get(
            game_version=game_version.name,
            spec_slug=spec.full_name_slug,
            boss_slug=key.boss.full_name_slug,
            difficulty=key.difficulty,
            metric=key.metric,
        )
        if ranking:
            pool.extend(player.talents for player in ranking.players if player.talents)
    return pool


async def load_spec_builds(payload: SpecBuildsPayload) -> tuple[bool, str]:  # ruff: ignore[unused-async]  # same interface as the other handlers
    """Work out the Builds of the spec from its stored Spec Rankings and save them."""
    game_version = payload.get_game_version()
    spec = game_version.data.get_spec(payload.spec_slug)
    if not spec or not spec.role.playable:
        raise TaskValidationError("invalid spec")
    scope = talent_trees.get_spec_scope(spec.id) if game_version.has_talents else None
    if scope is None:
        raise TaskValidationError("spec has no talents")

    pool = collect_pool(game_version, spec)
    logger.info(f"builds: {spec.full_name_slug} | {len(pool)} fights")
    if not pool:
        return True, "no data"

    result = spec_builds.find_builds(
        pool,
        spec_builds.TalentScope(*scope),
        ignore=spec.builds_ignore,
        force_new_build=spec.builds_force_new,
    )
    spec_builds.SpecBuilds.from_result(game_version.name, spec.full_name_slug, result).save()
    return True, "done"


async def main(message: dict[str, str]):
    """Work out the Builds of a spec."""
    message_body = message.get("body")
    if not message_body:
        raise TaskValidationError("No message body.")

    payload = SpecBuildsPayload.model_validate_json(message_body, extra="ignore")
    return await load_spec_builds(payload)
