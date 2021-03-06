#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import unittest
import testfixtures

from traits.api import Int
from traits.testing.api import UnittestTools
from force_bdss.core.input_slot_info import InputSlotInfo
from force_bdss.core.output_slot_info import OutputSlotInfo
from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel
from force_bdss.tests.dummy_classes.data_source import (
    DummyDataSource,
    DummyDataSourceModel,
)
from force_bdss.tests.dummy_classes.factory_registry import (
    DummyFactoryRegistry,
)

from unittest import mock

from force_bdss.data_sources.base_data_source_factory import (
    BaseDataSourceFactory,
)


class ChangesSlotsModel(BaseDataSourceModel):
    a = Int()
    b = Int(changes_slots=True)
    c = Int(changes_slots=False)


class BadDataSource(DummyDataSource):
    def slots(self, model):
        raise Exception("bad slots")


class TestBaseDataSourceModel(unittest.TestCase, UnittestTools):
    def setUp(self):
        self.mock_factory = mock.Mock(
            spec=BaseDataSourceFactory, plugin_id='dummy_id')
        self.mock_factory.id = "id"

    def test_getstate(self):
        model = DummyDataSourceModel(self.mock_factory)
        self.assertDictEqual(
            model.__getstate__(),
            {
                "id": "id",
                "model_data": {"input_slot_info": [], "output_slot_info": []},
            },
        )

        model.input_slot_info = [
            InputSlotInfo(name="foo"),
            InputSlotInfo(name="bar"),
        ]
        model.output_slot_info = [
            OutputSlotInfo(name="baz"),
            OutputSlotInfo(name="quux"),
        ]

        self.assertDictEqual(
            model.__getstate__(),
            {
                "id": "id",
                "model_data": {
                    "input_slot_info": [
                        {"source": "Environment", "name": "foo"},
                        {"source": "Environment", "name": "bar"},
                    ],
                    "output_slot_info": [{"name": "baz"}, {"name": "quux"}],
                },
            },
        )

    def test_changes_slots(self):
        model = ChangesSlotsModel(self.mock_factory)

        with self.assertTraitDoesNotChange(model, "changes_slots"):
            model.a = 5

        with self.assertTraitChanges(model, "changes_slots"):
            model.b = 5

        with self.assertTraitDoesNotChange(model, "changes_slots"):
            model.c = 5

    def test_bad_factory(self):
        def create_data_source():
            raise Exception("Bad data source factory")

        self.mock_factory.create_data_source = create_data_source
        model = DummyDataSourceModel(self.mock_factory)
        with testfixtures.LogCapture() as capture:
            with self.assertRaisesRegex(
                    Exception, "Bad data source factory"):
                model.verify()
            capture.check(
                ("force_bdss.data_sources.base_data_source_model",
                 "ERROR",
                 "Unable to create data source from factory "
                 "'id', plugin 'dummy_id'. This "
                 "might indicate a programming error")
            )

    def test_bad_slots(self):
        self.mock_factory.create_data_source = mock.MagicMock(
            return_value=BadDataSource(self.mock_factory)
        )
        model = DummyDataSourceModel(self.mock_factory)
        with testfixtures.LogCapture():
            with self.assertRaisesRegex(
                    Exception, "bad slots"):
                model.verify()

    def test_from_json(self):
        registry = DummyFactoryRegistry()
        factory = registry.data_source_factories[0]

        model_data = {
            "input_slot_info": [
                {"source": "Environment", "name": "foo"},
                {"source": "Environment", "name": "bar"},
            ],
            "output_slot_info": [{"name": "baz"}, {"name": "quux"}],
        }
        model = DummyDataSourceModel.from_json(factory, model_data)
        self.assertDictEqual(
            model.__getstate__(),
            {
                "model_data": model_data,
                "id": "force.bdss.enthought.plugin.test.v0.factory."
                      "dummy_data_source",
            },
        )
        # Test the initial dict did not change
        self.assertDictEqual(
            model_data,
            {
                "input_slot_info": [
                    {"source": "Environment", "name": "foo"},
                    {"source": "Environment", "name": "bar"},
                ],
                "output_slot_info": [{"name": "baz"}, {"name": "quux"}],
            },
        )
        # Test notification events
        with self.assertTraitChanges(model, "event", count=1):
            model.notify_start_event()
        with self.assertTraitChanges(model, "event", count=1):
            model.notify_finish_event()
