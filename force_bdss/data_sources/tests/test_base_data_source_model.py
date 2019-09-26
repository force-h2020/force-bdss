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

    def test___sync_slot_info(self):
        model = self.factory.create_model()

        old_info = InputSlotInfo(name="foo", type='GOOD')
        new_info = InputSlotInfo(name="bar", type='GOOD')

        model._sync_slot_info(new_info, old_info)

        self.assertEqual(new_info.name, old_info.name)

        wrong_class = OutputSlotInfo(name="foo", type='GOOD')
        with self.assertRaises(RuntimeError):
            model._sync_slot_info(wrong_class, old_info)

        wrong_type = InputSlotInfo(name="foo", type='BAD')
        with self.assertRaises(RuntimeError):
            model._sync_slot_info(wrong_type, old_info)

    def test_update_slot_info(self):

        model = self.factory.create_model()

        model.update_slot_info(
            "input_slot_info",
            [InputSlotInfo(name="bar")]
        )

        self.assertEqual("bar", model.input_slot_info[0].name)
        self.assertEqual("TYPE1", model.input_slot_info[0].type)

        with self.assertRaises(RuntimeError):
            model.update_slot_info(
                "wrong_attribute_name",
                [InputSlotInfo(name="bar")]
            )

        with self.assertRaises(RuntimeError):
            model.update_slot_info(
                "input_slot_info",
                [InputSlotInfo(name="bar"),
                 InputSlotInfo(name='too_long')]
            )

    def test_getstate(self):
        model = self.factory.create_model()

        self.assertDictEqual(
            model.__getstate__(),
            {
                "input_slot_info": [{'source': 'Environment',
                                     'description': 'No description',
                                     'name': '',
                                     'type': 'TYPE1'}],
                "output_slot_info": [{'name': '',
                                      'description': 'No description',
                                      'type': 'TYPE2'}]
            })

        model.input_slot_info[0].name = "foo"
        model.output_slot_info[0].name = "baz"

        self.assertDictEqual(
            model.__getstate__(),
            {
                "input_slot_info": [
                    {
                        "source": "Environment",
                        "name": "foo",
                        'type': 'TYPE1',
                        'description': 'No description'
                    }
                ],
                "output_slot_info": [
                    {
                        "name": "baz",
                        "type": 'TYPE2',
                        'description': 'No description'
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
        model = DummyDataSourceModel(factory)

        with self.assertRaises(Exception):
            model.verify()

    def test_bad_slots(self):

        model = DummyDataSourceModel(self.factory)

        with mock.patch('force_bdss.tests.dummy_classes.data_source.'
                        'DummyDataSourceFactory.create_data_source')\
                as mock_data_source:
            mock_data_source.return_value = BadDataSource(self.factory)
            with self.assertRaises(Exception):
                model.verify()

    def test___reset_data_source_slots(self):

        model = self.factory.create_model()
        model.input_slot_info[0].name = 'foo'

        model._reset_data_source_slots()

        self.assertEqual('', model.input_slot_info[0].name)

    def test_verify(self):

        model = DummyDataSourceModel(self.factory)

        model.input_slot_info = [
            InputSlotInfo(name="bar"),
            InputSlotInfo(name='too_long')
        ]

        errors = model.verify()
        messages = [error.local_error for error in errors]

        self.assertIn("The number of input slots is incorrect.",
                      messages)
        self.assertIn("All output variables have undefined names.",
                      messages)

        model.output_slot_info = []

        errors = model.verify()
        messages = [error.local_error for error in errors]
        self.assertIn("The number of output slots is incorrect.",
                      messages)
        self.assertNotIn("All output variables have undefined names.",
                         messages)
