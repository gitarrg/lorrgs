"""Handler to Load Spec Rankings."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import datetime

# IMPORT LOCAL LIBRARIES
from lorgs import data  # pylint: disable=unused-import  # noqa: F401
from lorgs.loaders.spec_ranking import SpecRankingLoader
from lorgs.logger import logger
from lorgs.models import warcraftlogs_ranking
from lorgs.models.task_payloads import SpecRankingPayload
from lorrgs_sqs.exceptions import TaskValidationError


async def load_spec_rankings(payload: SpecRankingPayload) -> tuple[bool, str]:
    """Load the Spec Ranking Data from Warcraftlogs and save it to the Database."""
    logger.info(f"loading: {payload} vs {payload.spec_slug} | {payload.difficulty=}")

    ################################
    # get spec ranking object
    ranking = warcraftlogs_ranking.SpecRanking.get_or_create(
        boss_slug=payload.boss_slug,
        spec_slug=payload.spec_slug,
        difficulty=payload.difficulty,
        metric=payload.metric,
    )
    if not ranking.boss:
        raise TaskValidationError("invalid boss")
    if not ranking.spec:
        raise TaskValidationError("invalid spec")

    clear = payload.clear

    # force refresh if dirty
    if ranking.dirty:
        clear = True

    # skip if updated recently
    if not clear:
        now = datetime.datetime.now(datetime.UTC)
        updated = ranking.updated
        # Some persisted/initialized values may be offset-naive; treat them as UTC.
        if updated.tzinfo is None:
            updated = updated.replace(tzinfo=datetime.UTC)

        try:
            if updated > (now - datetime.timedelta(hours=2)):
                return True, "already updated"
        except TypeError:
            logger.warning(f"Failed to compare timestamp ({now=}, {updated=}) for {payload=}")

    ################################
    # load and save
    await SpecRankingLoader(ranking).load(limit=payload.limit, clear_old=clear)
    ranking.save()
    return True, "done"


async def main(message: dict[str, str]):
    """Load the Spec Ranking Data from Warcraftlogs and save it to the Database."""

    message_body = message.get("body")
    if not message_body:
        raise TaskValidationError("No message body.")

    payload = SpecRankingPayload.model_validate_json(message_body, extra="ignore")
    return await load_spec_rankings(payload)
