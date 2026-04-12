"""Handler to Load Comp Rankings."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import json

# IMPORT LOCAL LIBRARIES
from lorgs import data  # pylint: disable=unused-import  # noqa: F401
from lorgs.logger import logger
from lorgs.models import warcraftlogs_comp_ranking
from lorrgs_sqs.exceptions import TaskValidationError


async def load_comp_rankings(boss_slug: str, page=1, clear=False) -> tuple[bool, str]:
    """Load the Comp Ranking Data from Warcraftlogs and save it to the Database."""
    ################################
    # Get inputs
    logger.info(f"loading: {boss_slug} | ({page=} / {clear=})")
    if boss_slug is None:
        raise TaskValidationError(f"missing boss: {boss_slug}")

    ################################
    # get comp ranking object
    ranking = warcraftlogs_comp_ranking.CompRanking.get_or_create(boss_slug=boss_slug)
    if not ranking.boss:
        raise TaskValidationError("invalid boss")

    ################################
    # load and save
    await ranking.load(page=page, clear_old=clear)
    ranking.save()
    return True, "done"


async def main(message: dict[str, str]):
    """Load the Spec Ranking Data from Warcraftlogs and save it to the Database."""

    # parse the message
    message_body = message.get("body")
    if not message_body:
        raise TaskValidationError("No message body.")
    payload = json.loads(message_body)

    return await load_comp_rankings(
        boss_slug=payload.get("boss_slug"),
        page=payload.get("page", 1),
        clear=payload.get("clear", False),
    )
