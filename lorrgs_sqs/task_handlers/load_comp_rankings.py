"""Handler to Load Comp Rankings."""

from __future__ import annotations

# IMPORT LOCAL LIBRARIES
from lorgs import data  # pylint: disable=unused-import  # noqa: F401
from lorgs.logger import logger
from lorgs.models import warcraftlogs_comp_ranking
from lorgs.models.task_payloads import CompRankingPayload
from lorrgs_sqs.exceptions import TaskValidationError


async def load_comp_rankings(payload: CompRankingPayload) -> tuple[bool, str]:
    """Load the Comp Ranking Data from Warcraftlogs and save it to the Database."""
    logger.info(f"loading: {payload}")

    ################################
    # get comp ranking object
    ranking = warcraftlogs_comp_ranking.CompRanking.get_or_create(boss_slug=payload.boss_slug)
    if not ranking.boss:
        raise TaskValidationError("invalid boss")

    ################################
    # load and save
    await ranking.load(page=payload.page, clear_old=payload.clear)
    ranking.save()
    return True, "done"


async def main(message: dict[str, str]):
    """Load the Comp Ranking Data from Warcraftlogs and save it to the Database."""
    message_body = message.get("body")
    if not message_body:
        raise TaskValidationError("No message body.")

    payload = CompRankingPayload.model_validate_json(message_body, extra="ignore")
    return await load_comp_rankings(payload)
