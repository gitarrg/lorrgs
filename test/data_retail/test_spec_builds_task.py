import asyncio
import json

from lorgs.data import RETAIL
from lorgs.models import spec_builds, warcraftlogs_ranking
from lorgs.models.task_payloads import SpecBuildsPayload
from lorgs.models.wow_spec import WowSpec
from lorrgs_sqs import helpers
from lorrgs_sqs.task_handlers import load_spec_builds


class FakeRanking:
    def __init__(self, talents):
        self.players = [type("P", (), {"talents": t})() for t in talents]


def test_all_expands_to_playable_specs():
    payload = SpecBuildsPayload(game_version="retail", spec_slug="all").model_dump()
    payloads = helpers.expand_keywords(payload)

    slugs = {p["spec_slug"] for p in payloads}
    assert "priest-shadow" in slugs
    assert not any(slug.startswith("other-") for slug in slugs)
    assert all(p["task"] == "load_spec_builds" for p in payloads)


def test_load_spec_builds_saves_builds_of_all_rankings(monkeypatch):
    spec = RETAIL.data.get_spec("priest-shadow")
    assert isinstance(spec, WowSpec)

    requested = []

    def fake_get(cls, **kwargs):
        requested.append((kwargs["boss_slug"], kwargs["difficulty"], kwargs["metric"]))
        return FakeRanking([{101: 1}, {}])  # a player without talents is left out

    saved = []
    monkeypatch.setattr(warcraftlogs_ranking.SpecRanking, "get", classmethod(fake_get))
    monkeypatch.setattr(spec_builds.SpecBuilds, "save", lambda self: saved.append(self))

    message = {
        "body": json.dumps({"task": "load_spec_builds", "game_version": "retail", "spec_slug": spec.full_name_slug})
    }
    assert asyncio.run(load_spec_builds.main(message)) == (True, "done")

    bosses = {boss for boss, _, _ in requested}
    assert bosses == {boss.full_name_slug for boss in RETAIL.data.bosses}
    assert {metric for _, _, metric in requested} == {spec.role.metric}
    assert len(saved) == 1
    assert saved[0].spec_slug == spec.full_name_slug
    assert saved[0].fights == len(requested)


def test_no_stored_rankings_saves_nothing(monkeypatch):
    saved = []
    monkeypatch.setattr(warcraftlogs_ranking.SpecRanking, "get", classmethod(lambda cls, **kwargs: None))
    monkeypatch.setattr(spec_builds.SpecBuilds, "save", lambda self: saved.append(self))

    payload = SpecBuildsPayload(game_version="retail", spec_slug="priest-shadow")
    assert asyncio.run(load_spec_builds.load_spec_builds(payload)) == (True, "no data")
    assert saved == []
