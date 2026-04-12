"""Handler to Load Spec Rankings."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import datetime
import json

# IMPORT LOCAL LIBRARIES
from lorgs import data  # pylint: disable=unused-import  # noqa: F401
from lorgs.logger import logger
from lorgs.models import warcraftlogs_ranking
from lorrgs_sqs.exceptions import TaskValidationError


async def load_spec_rankings(
    boss_slug: str,
    spec_slug: str,
    difficulty: str = "mythic",
    metric: str = "dps",
    limit=50,
    clear=False,
) -> tuple[bool, str]:
    """Load the Spec Ranking Data from Warcraftlogs and save it to the Database."""
    ################################
    # Get inputs

    logger.info(f"loading: {boss_slug} vs {spec_slug} | ({difficulty=} / {metric=} / {limit=} / {clear=})")
    if boss_slug is None or spec_slug is None:
        raise TaskValidationError(f"missing boss or spec ({boss_slug} / {spec_slug})")

    ################################
    # get spec ranking object
    ranking = warcraftlogs_ranking.SpecRanking.get_or_create(
        boss_slug=boss_slug,
        spec_slug=spec_slug,
        difficulty=difficulty,
        metric=metric,
    )
    if not ranking.boss:
        raise TaskValidationError("invalid boss")
    if not ranking.spec:
        raise TaskValidationError("invalid spec")

    # force refresh if dirty
    if ranking.dirty:
        clear = True

    # skip if updated recently
    if not clear:
        now = datetime.datetime.now(datetime.timezone.utc)
        updated = ranking.updated
        # Some persisted/initialized values may be offset-naive; treat them as UTC.
        if updated.tzinfo is None:
            updated = updated.replace(tzinfo=datetime.timezone.utc)

        try:
            if updated > (now - datetime.timedelta(hours=2)):
                return True, "already updated"
        except:
            pass

    ################################
    # load and save
    await ranking.load(limit=limit, clear_old=clear)
    ranking.save()
    return True, "done"


async def main(message: dict[str, str]):
    """Load the Spec Ranking Data from Warcraftlogs and save it to the Database."""

    # parse the message
    message_body = message.get("body")
    if not message_body:
        raise TaskValidationError("No message body.")
    payload = json.loads(message_body)

    return await load_spec_rankings(
        boss_slug=payload.get("boss_slug"),
        spec_slug=payload.get("spec_slug"),
        difficulty=payload.get("difficulty", "mythic"),
        metric=payload.get("metric", "dps"),
        limit=payload.get("limit", 50),
        clear=payload.get("clear", False),
    )
