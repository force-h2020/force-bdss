import testfixtures
from unittest import TestCase, mock

from traits.api import Int
from traits.testing.api import UnittestTools

from force_bdss.core.input_slot_info import InputSlotInfo
from force_bdss.core.slot import Slot
from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel
from force_bdss.data_sources.data_source_utilities import TraitSimilarityError
from force_bdss.tests.dummy_classes.data_source import (
    DummyDataSourceFactory, DummyDataSource, DummyDataSourceModel
)
from force_bdss.tests.dummy_classes.extension_plugin import (
    DummyExtensionPlugin
)
from force_bdss.tests.probe_classes.probe_extension_plugin import (
    ProbeExtensionPlugin
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
        self.probe_plugin = ProbeExtensionPlugin()
        self.probe_factory = self.probe_plugin.data_source_factories[0]

        self.dummy_plugin = DummyExtensionPlugin()
        self.dummy_factory = self.dummy_plugin.data_source_factories[0]

    def test_init(self):

        # Empty initialisation
        model = self.dummy_factory.create_model()

        self.assertEqual(1, len(model.input_slot_info))
        self.assertEqual(1, len(model.output_slot_info))

        self.assertEqual("", model.input_slot_info[0].name)
        self.assertEqual("TYPE1", model.input_slot_info[0].type)
        self.assertEqual(
            "No description", model.input_slot_info[0].description
        )

        self.assertEqual("", model.output_slot_info[0].name)
        self.assertEqual("TYPE2", model.output_slot_info[0].type)
        self.assertEqual(
            "No description", model.output_slot_info[0].description
        )

        # Initialise with model_data - In this example the type attribute
        # must match that returned by DummyDataSource class, but both `name`
        # and `description` are free to be assigned
        model_data = {
            "input_slot_info": [
                InputSlotInfo(name="foo",
                              type="TYPE1",
                              description="A description")
            ]}
        model = self.dummy_factory.create_model(model_data=model_data)

        self.assertEqual(1, len(model.input_slot_info))
        self.assertEqual(1, len(model.output_slot_info))

        self.assertEqual("foo", model.input_slot_info[0].name)
        self.assertEqual("TYPE1", model.input_slot_info[0].type)
        self.assertEqual(
            "A description", model.input_slot_info[0].description)

        self.assertEqual("", model.output_slot_info[0].name)
        self.assertEqual("TYPE2", model.output_slot_info[0].type)
        self.assertEqual(
            "No description", model.output_slot_info[0].description)

    def test_init_exceptions(self):

        with testfixtures.LogCapture() as capture:
            # Initialise with incorrect length of input_slot_info
            with self.assertRaises(ValueError):
                model_data = {
                    "input_slot_info": [
                        InputSlotInfo(), InputSlotInfo()
                    ]}
                self.probe_factory.create_model(model_data=model_data)
            capture.check(
                ('force_bdss.data_sources.base_data_source_model',
                 'ERROR',
                 "The number of InputSlotInfo objects (2) "
                 "of the ProbeDataSourceModel model doesn't match"
                 " the expected number of slots (1). This is likely "
                 'due to a corrupted file.')
            )
            capture.clear()

            # Initialise with incorrect `type` attribute on
            # input_slot_info element
            with self.assertRaises(TraitSimilarityError):
                model_data = {
                    "input_slot_info": [
                        InputSlotInfo(type="WRONG_TYPE")
                    ]}
                self.probe_factory.create_model(model_data=model_data)
            capture.check(
                ('force_bdss.data_sources.data_source_utilities',
                 'ERROR',
                 'Source object has failed a trait similarity check '
                 'with target: The type attribute of source (WRONG_TYPE)'
                 " doesn't match target (PRESSURE).")
            )
            capture.clear()

            # Initialise with incorrect `description` attribute on
            # input_slot_info element
            with self.assertRaises(TraitSimilarityError):
                model_data = {
                    "input_slot_info": [
                        InputSlotInfo(description="Wrong description")
                    ]}
                self.probe_factory.create_model(model_data=model_data)
            capture.check(
                ('force_bdss.data_sources.data_source_utilities',
                 'ERROR',
                 'Source object has failed a trait similarity check '
                 'with target: The description attribute of source'
                 " (Wrong description) doesn't match "
                 "target (An input variable).")
            )
            capture.clear()

    def test__assign_slot_info(self):

        # Test normal function
        model = self.dummy_factory.create_model()
        model._assign_slot_info()

        self.assertEqual("", model.input_slot_info[0].name)
        self.assertEqual("TYPE1", model.input_slot_info[0].type)
        self.assertEqual(
            "No description", model.input_slot_info[0].description
        )

        # Test with new attribute values on InputSlotInfo object
        model.input_slot_info[0].name = 'foo'
        model.input_slot_info[0].description = 'A variable'
        model._assign_slot_info()

        self.assertEqual("foo", model.input_slot_info[0].name)
        self.assertEqual("TYPE1", model.input_slot_info[0].type)
        self.assertEqual("A variable", model.input_slot_info[0].description)

        # Test with default values on Slot object
        with mock.patch('force_bdss.data_sources.base_data_source_model.'
                        'BaseDataSourceModel._data_source_slots',
                        return_value=([Slot()], [Slot()])):
            model._assign_slot_info()

            self.assertEqual("foo", model.input_slot_info[0].name)
            self.assertEqual("TYPE1", model.input_slot_info[0].type)
            self.assertEqual(
                "A variable", model.input_slot_info[0].description
            )

        # Test with empty list for output_slot_info attribute
        model.output_slot_info = []
        model._assign_slot_info()

        self.assertEqual("", model.output_slot_info[0].name)
        self.assertEqual("TYPE2", model.output_slot_info[0].type)
        self.assertEqual(
            "No description", model.output_slot_info[0].description
        )

    def test_getstate(self):
        model = self.dummy_factory.create_model()

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
        model = ChangesSlotsModel(self.dummy_factory)

        with self.assertTraitDoesNotChange(model, "changes_slots"):
            model.a = 5

        with self.assertTraitChanges(model, "changes_slots"):
            model.b = 5

        with self.assertTraitDoesNotChange(model, "changes_slots"):
            model.c = 5

    def test_bad_slots(self):

        model = DummyDataSourceModel(self.dummy_factory)

        with mock.patch('force_bdss.tests.dummy_classes.data_source.'
                        'DummyDataSourceFactory.create_data_source')\
                as mock_data_source:
            mock_data_source.return_value = BadDataSource(self.dummy_factory)
            with testfixtures.LogCapture():
                with self.assertRaises(Exception):
                    model.verify()

    def test_verify(self):

        model = DummyDataSourceModel(self.dummy_factory)

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
