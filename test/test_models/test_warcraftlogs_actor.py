import sys
import unittest
from unittest import mock

import pytest

from lorgs.loaders.actor_loader import ActorLoader
from lorgs.models.warcraftlogs_actor import BaseActor
from lorgs.models import wow_class
from lorgs.models import wow_role
from lorgs.models import wow_spec

from test import helpers


# Test Classes
# todo: move somewhere else or mock away
MOCK_ROLE = wow_role.WowRole(id=4, name="Test", code="test")
MOCK_CLASS = wow_class.WowClass(id=4, name="Test")
MOCK_SPEC = wow_spec.WowSpec(name="TestSpec", wow_class=MOCK_CLASS, role=MOCK_ROLE)


class TestBaseActor(unittest.TestCase):
    @mock.patch.multiple(BaseActor, __abstractmethods__=set())
    def setUp(self):
        self.actor = BaseActor()

    ################################
    # source id

    def test_has_source_id_true(self):
        self.actor.source_id = 5
        assert self.actor._has_source_id == True

    def test_has_source_id_false(self):
        assert self.actor._has_source_id == False
        self.actor.source_id = -1
        assert self.actor._has_source_id == False


class TestActorLoaderProcess(unittest.TestCase):
    """Test processing the query result via the loader."""

    @mock.patch.multiple(BaseActor, __abstractmethods__=set())
    def setUp(self):
        self.actor = BaseActor()
        self.loader = ActorLoader(self.actor)

    def test__process_casts__simple(self):
        casts_events = [
            {
                "timestamp": 1001,
                "type": "cast",
                "sourceID": 10,
                "abilityGameID": 101,
            },
            {
                "timestamp": 1002,
                "type": "cast",
                "sourceID": 10,
                "abilityGameID": 102,
            },
            {
                "timestamp": 1010,
                "type": "cast",
                "sourceID": 10,
                "abilityGameID": 103,
            },
        ]
        casts_data = helpers.wrap_data(casts_events, "report", "events", "data")

        self.actor.source_id = 10
        self.loader.process_query_result(casts_data)

        assert self.actor.casts != []
        assert len(self.actor.casts) == 3

        cast = self.actor.casts[2]
        assert cast.spell_id == 103
        assert cast.timestamp == 1010

    def test__process_casts__ignore_other_source_ids(self):
        """Make sure a cast from another ID is not added"""
        casts_events = [{"sourceID": 123}]
        casts_data = helpers.wrap_data(casts_events, "report", "events", "data")

        assert not self.actor.casts
        self.actor.source_id = 10
        self.loader.process_query_result(casts_data)
        assert not self.actor.casts


if __name__ == "__main__":
    pytest.main(sys.argv)
