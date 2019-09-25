from unittest import TestCase, mock

from traits.api import Int
from traits.testing.api import UnittestTools

from force_bdss.core.input_slot_info import InputSlotInfo
from force_bdss.core.output_slot_info import OutputSlotInfo
from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel
from force_bdss.tests.dummy_classes.data_source import (
    DummyDataSourceFactory, DummyDataSource, DummyDataSourceModel
)
from force_bdss.tests.dummy_classes.extension_plugin import (
    DummyExtensionPlugin
)


class ChangesSlotsModel(BaseDataSourceModel):
    a = Int()
    b = Int(changes_slots=True)
    c = Int(changes_slots=False)


class BadDataSourceFactory(DummyDataSourceFactory):

    def create_data_source(self):
        raise Exception("Bad data source factory")


class BadDataSource(DummyDataSource):

    def slots(self, model):
        print('exception')
        raise Exception("bad slots")


class TestBaseDataSourceModel(TestCase, UnittestTools):
    def setUp(self):
        self.plugin = DummyExtensionPlugin()
        self.factory = self.plugin.data_source_factories[0]

    def test_getstate(self):
        model = self.factory.create_model()

        self.assertDictEqual(
            model.__getstate__(),
            {
                "input_slot_info": [{'source': 'Environment',
                                     'name': '',
                                     'type': 'TYPE1'}],
                "output_slot_info": [{'name': '',
                                      'type': 'TYPE2'}]
            })

        model.input_slot_info = [
            InputSlotInfo(name="foo")
        ]
        model.output_slot_info = [
            OutputSlotInfo(name="baz")
        ]

        self.assertDictEqual(
            model.__getstate__(),
            {
                "input_slot_info": [
                    {
                        "source": "Environment",
                        "name": "foo",
                        'type': 'TYPE1'
                    }
                ],
                "output_slot_info": [
                    {
                        "name": "baz",
                        "type": 'TYPE2'
                    }
                ]
            })

    def test_changes_slots(self):
        model = ChangesSlotsModel(self.factory)

        with self.assertTraitDoesNotChange(model, "changes_slots"):
            model.a = 5

        with self.assertTraitChanges(model, "changes_slots"):
            model.b = 5

        with self.assertTraitDoesNotChange(model, "changes_slots"):
            model.c = 5

    def test_bad_factory(self):

        factory = BadDataSourceFactory(self.plugin)
        with self.assertRaises(Exception):
            DummyDataSourceModel(factory)

    def test_bad_slots(self):

        with mock.patch('force_bdss.tests.dummy_classes.data_source.'
                        'DummyDataSourceFactory.create_data_source')\
                as mock_data_source:
            mock_data_source.return_value = BadDataSource(self.factory)
            with self.assertRaises(Exception):
                DummyDataSourceModel(self.factory)
