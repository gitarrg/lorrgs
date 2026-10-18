import unittest
from unittest import mock

from lorgs.models.base.dynamodb import DynamoDBModel
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_user_report import UserReport


class TestUserReport(unittest.TestCase):
    def setUp(self):
        self.user_report = UserReport(report_id="REPORT_ID")

    def test__is_loaded__yes(self):
        self.user_report.fights = [Fight.model_construct(fight_id=1)]
        assert self.user_report.is_loaded

    def test__is_loaded__nope(self):
        self.user_report.fights = []
        assert not self.user_report.is_loaded

    def test__save__updates_timestamp(self):
        prev_value = self.user_report.updated

        with mock.patch.object(DynamoDBModel, "save"):
            self.user_report.save()

        assert self.user_report.updated != prev_value
