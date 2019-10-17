import testfixtures
from unittest import TestCase, mock

from traits.api import Int
from traits.testing.api import UnittestTools

from force_bdss.core.input_slot_info import InputSlotInfo
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
        raise Exception("bad slots")


class TestBaseDataSourceModel(TestCase, UnittestTools):
    def setUp(self):
        self.plugin = DummyExtensionPlugin()
        self.factory = self.plugin.data_source_factories[0]

    def test__assign_slot_info(self):

        # Test normal function
        model = self.factory.create_model()
        model._assign_slot_info(
            "input_slot_info",
            [InputSlotInfo(name="bar")]
        )
        self.assertEqual("bar", model.input_slot_info[0].name)
        self.assertEqual("TYPE1", model.input_slot_info[0].type)

        with testfixtures.LogCapture() as capture:
            # Test name argument failure
            with self.assertRaises(ValueError):
                model._assign_slot_info(
                    "wrong_argument_name",
                    [InputSlotInfo(name="bar")]
                )
            capture.check(
                ('force_bdss.data_sources.base_data_source_model',
                 'ERROR',
                 "Attribute 'name' must be either "
                 "'input_slot_info' or 'output_slot_info'.")
            )
            capture.clear()

            # Wrong Slot type attribute
            with self.assertRaises(RuntimeError):
                model._assign_slot_info(
                    "input_slot_info",
                    [InputSlotInfo(name="bar",
                                   type='wrong_type')]
                )
            capture.check(
                ('force_bdss.data_sources.data_source_utilities',
                 'ERROR',
                 'The type attribute of source <class '
                 "'force_bdss.core.input_slot_info.InputSlotInfo'> "
                 "(wrong_type) doesn't match the target <class "
                 "'force_bdss.core.input_slot_info.InputSlotInfo'> (TYPE1).")
            )
            capture.clear()

            # Wrong Slot description attribute
            with self.assertRaises(RuntimeError):
                model._assign_slot_info(
                    "input_slot_info",
                    [InputSlotInfo(name="bar",
                                   description='wrong_desc')]
                )
            capture.check(
                ('force_bdss.data_sources.data_source_utilities',
                 'ERROR',
                 'The description attribute of source <class '
                 "'force_bdss.core.input_slot_info.InputSlotInfo'> "
                 "(wrong_desc) doesn't match the target <class "
                 "'force_bdss.core.input_slot_info.InputSlotInfo'> "
                 "(No description).")
            )
            capture.clear()

            # Wrong slot length
            with self.assertRaises(RuntimeError):
                model._assign_slot_info(
                    "input_slot_info",
                    [InputSlotInfo(name="bar"),
                     InputSlotInfo(name='too_long')]
                )
            capture.check(
                ('force_bdss.data_sources.base_data_source_model',
                 'ERROR',
                 'The number of slots in input_slot_info (1) of the '
                 "DummyDataSourceModel model doesn't match the "
                 "expected number of slots (2). This is likely due to "
                 'a corrupted file.')
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
            with testfixtures.LogCapture():
                with self.assertRaises(Exception):
                    model.verify()

    def test_slot_info_defaults(self):

        model = DummyDataSourceModel(self.factory)
        input_slot_info, output_slot_info = model.slot_info_defaults()

        self.assertEqual(1, len(input_slot_info))
        self.assertEqual(1, len(output_slot_info))

        self.assertEqual('TYPE1', input_slot_info[0].type)
        self.assertEqual('TYPE2', output_slot_info[0].type)

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
