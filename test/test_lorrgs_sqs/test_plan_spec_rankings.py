import asyncio
import datetime
import types

from lorgs.models import ranking_status
from lorgs.models.task_payloads import SpecRankingPayload
from lorrgs_sqs.task_handlers import plan_spec_rankings as handler


def _payload(spec: str) -> SpecRankingPayload:
    return SpecRankingPayload(
        game_version="retail", spec_slug=spec, boss_slug="boss", difficulty="heroic", metric="dps"
    )


def _run(monkeypatch, *, last_modified, dirty, dry_run=False):
    sent: list[tuple[list, str]] = []
    payloads = {f"retail/{spec}": _payload(spec) for spec in ("a", "b", "c")}

    class Client:
        async def get_rate_info(self):
            return {"limitPerHour": 40 * 2 / 0.8, "pointsSpentThisHour": 0}  # budget: 2 Refreshes

    monkeypatch.setattr(handler.WarcraftlogsClient, "get_instance", lambda: Client())
    monkeypatch.setattr(
        handler,
        "GAME_VERSIONS",
        {
            "retail": types.SimpleNamespace(
                name="retail", updates_enabled=True, data=types.SimpleNamespace(get_spec=lambda slug: None)
            )
        },
    )
    monkeypatch.setattr(handler, "get_ranking_payloads", lambda game_version: payloads)
    monkeypatch.setattr(ranking_status, "list_last_modified", lambda game_version: last_modified)
    monkeypatch.setattr(ranking_status.DirtyMarker, "list_flagged", lambda game_version: dirty)
    monkeypatch.setattr(
        handler.sqs,
        "send_message_batch",
        lambda payloads, message_group="", **kw: sent.append((list(payloads), message_group)),
    )
    result = asyncio.run(handler.plan_spec_rankings(dry_run=dry_run))
    return result, sent


def test_queues_stalest_first_within_budget(monkeypatch):
    now = datetime.datetime.now(datetime.UTC)
    last_modified = {
        "retail/a": now - datetime.timedelta(hours=1),
        "retail/b": now - datetime.timedelta(hours=9),
        "retail/c": now - datetime.timedelta(hours=5),
    }
    _, sent = _run(monkeypatch, last_modified=last_modified, dirty={})

    assert len(sent) == 1
    payloads, group = sent[0]
    assert [p.spec_slug for p in payloads] == ["b", "c"]
    assert group == "retail-load_spec_rankings"
    assert all(p.limit == 50 and not p.clear and not p.dirty for p in payloads)


def test_dirty_rankings_are_queued_as_dirty(monkeypatch):
    now = datetime.datetime.now(datetime.UTC)
    _, sent = _run(monkeypatch, last_modified={}, dirty={"retail/c": now})

    payloads, _ = sent[0]
    assert payloads[0].spec_slug == "c"
    assert payloads[0].dirty


def test_dry_run_queues_nothing(monkeypatch):
    _, sent = _run(monkeypatch, last_modified={}, dirty={}, dry_run=True)
    assert sent == []
