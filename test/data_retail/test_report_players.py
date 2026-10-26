"""Players found in a Report's master data are matched to Retail specs."""

import datetime
import unittest

import lorgs.data  # noqa: F401  # registers specs
from lorgs.clients import wcl
from lorgs.loaders.report_overview_loader import ReportOverviewLoader
from lorgs.models.warcraftlogs_report import Report


class TestReportPlayers(unittest.TestCase):
    def setUp(self) -> None:
        self.report = Report(
            report_id="REPORT_ID",
            start_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.UTC),
        )
        self.loader = ReportOverviewLoader(self.report)

    def test_player_from_actor_data(self):
        actor = wcl.ReportActor(
            id=32,
            name="PlayerName",
            icon="Shaman-Restoration",
            type="Player",
            subType="Shaman",
        )
        player = self.loader._player_from_actor_data(actor)
        assert player is not None
        assert player.source_id == 32
        assert player.name == "PlayerName"
        assert player.spec_slug == "shaman-restoration"
        assert player.class_slug == "shaman"

    def test_player_from_actor_data_unknown_spec(self):
        actor = wcl.ReportActor(id=5, name="HunterPlayer", icon="Hunter", subType="Hunter")
        player = self.loader._player_from_actor_data(actor)
        assert player is not None
        assert player.spec_slug == ""
        assert player.class_slug == "hunter"
