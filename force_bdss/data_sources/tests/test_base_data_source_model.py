import unittest

from traits.api import Int
from traits.testing.api import UnittestTools
from force_bdss.core.input_slot_info import InputSlotInfo
from force_bdss.core.output_slot_info import OutputSlotInfo
from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel
from force_bdss.tests.dummy_classes.data_source import DummyDataSourceModel

from unittest import mock

from force_bdss.data_sources.base_data_source_factory import \
    BaseDataSourceFactory


class ChangesSlotsModel(BaseDataSourceModel):
    a = Int()
    b = Int(changes_slots=True)
    c = Int(changes_slots=False)


class TestBaseDataSourceModel(unittest.TestCase, UnittestTools):
    def setUp(self):
        self.mock_factory = mock.Mock(spec=BaseDataSourceFactory)

    def test_getstate(self):
        model = DummyDataSourceModel(self.mock_factory)
        self.assertEqual(
            model.__getstate__(),
            {
                "__traits_version__": "4.6.0",
                "input_slot_info": [],
                "output_slot_info": []
            })

        model.input_slot_info = [
            InputSlotInfo(
                name="foo"
            ),
            InputSlotInfo(
                name="bar"
            )
        ]
        model.output_slot_info = [
            OutputSlotInfo(name="baz"),
            OutputSlotInfo(name="quux")
        ]

        self.assertEqual(
            model.__getstate__(),
            {
                "__traits_version__": "4.6.0",
                "input_slot_info": [
                    {
                        "__traits_version__": "4.6.0",
                        "source": "Environment",
                        "name": "foo"
                    },
                    {
                        "__traits_version__": "4.6.0",
                        "source": "Environment",
                        "name": "bar"
                    }
                ],
                "output_slot_info": [
                    {
                        "__traits_version__": "4.6.0",
                        "name": "baz",
                    },
                    {
                        "__traits_version__": "4.6.0",
                        "name": "quux",
                    }
                ]
            })

    def test_changes_slots(self):
        model = ChangesSlotsModel(self.mock_factory)

        with self.assertTraitDoesNotChange(model, "changes_slots"):
            model.a = 5

        with self.assertTraitChanges(model, "changes_slots"):
            model.b = 5

        with self.assertTraitDoesNotChange(model, "changes_slots"):
            model.c = 5
