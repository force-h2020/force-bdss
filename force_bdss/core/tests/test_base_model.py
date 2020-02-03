from unittest import TestCase

from traits.testing.unittest_tools import UnittestTools

from force_bdss.core.base_model import BaseModel
from force_bdss.events.base_driver_event import BaseDriverEvent
from force_bdss.tests.dummy_classes.mco import DummyMCOFactory


class TestBaseModel(TestCase, UnittestTools):

    def setUp(self):
        self.factory = DummyMCOFactory(
            {"id": "pid", "name": "test"}
        )
        self.model = BaseModel(self.factory)

    def test_notify(self):
        with self.assertTraitChanges(
                self.model, 'event', count=1):
            self.model.notify(BaseDriverEvent())
