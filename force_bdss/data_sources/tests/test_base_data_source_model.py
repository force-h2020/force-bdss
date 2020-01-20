import unittest

from traits.api import Int
from traits.testing.api import UnittestTools
from force_bdss.core.input_slot_info import InputSlotInfo
from force_bdss.core.output_slot_info import OutputSlotInfo
from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel
from force_bdss.tests.dummy_classes.data_source import (
    DummyDataSource,
    DummyDataSourceModel,
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
        self.mock_factory = mock.Mock(spec=BaseDataSourceFactory)
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
        def create_data_source(self):
            raise Exception("Bad data source factory")

        self.mock_factory.create_data_source = create_data_source
        model = DummyDataSourceModel(self.mock_factory)
        with self.assertRaises(Exception):
            model.verify()

    def test_bad_slots(self):
        self.mock_factory.create_data_source = mock.MagicMock(
            return_value=BadDataSource(self.mock_factory)
        )
        model = DummyDataSourceModel(self.mock_factory)
        with self.assertRaises(Exception):
            model.verify()

    def test_fromjson(self):
        model_data = {
            "input_slot_info": [
                {"source": "Environment", "name": "foo"},
                {"source": "Environment", "name": "bar"},
            ],
            "output_slot_info": [{"name": "baz"}, {"name": "quux"}],
        }
        model = DummyDataSourceModel.from_json(self.mock_factory, model_data)
        self.assertDictEqual(
            model.__getstate__(), {"model_data": model_data, "id": "id"}
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
