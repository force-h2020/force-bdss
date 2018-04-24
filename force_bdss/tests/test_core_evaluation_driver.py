import unittest

import testfixtures
import six

from force_bdss.tests.probe_classes.factory_registry_plugin import \
    ProbeFactoryRegistryPlugin
from force_bdss.tests.probe_classes.mco import ProbeMCOFactory
from force_bdss.tests.probe_classes.data_source import ProbeDataSourceFactory
from force_bdss.tests.probe_classes.kpi_calculator import (
    ProbeKPICalculatorFactory)

from force_bdss.core.input_slot_map import InputSlotMap
from force_bdss.core.data_value import DataValue
from force_bdss.core.slot import Slot
from force_bdss.tests import fixtures

try:
    import mock
except ImportError:
    from unittest import mock

from envisage.api import Application

from force_bdss.core_evaluation_driver import CoreEvaluationDriver, \
    _bind_data_values, _compute_layer_results


class TestCoreEvaluationDriver(unittest.TestCase):
    def setUp(self):
        self.factory_registry_plugin = ProbeFactoryRegistryPlugin()
        application = mock.Mock(spec=Application)
        application.get_plugin = mock.Mock(
            return_value=self.factory_registry_plugin
        )
        application.workflow_filepath = fixtures.get("test_null.json")
        self.mock_application = application

    def test_initialization(self):
        driver = CoreEvaluationDriver(
            application=self.mock_application,
        )
        driver.application_started()

    def test_error_for_non_matching_mco_parameters(self):
        mco_factories = self.factory_registry_plugin.mco_factories
        mco_factories[0] = ProbeMCOFactory(
            None,
            nb_output_data_values=1)
        driver = CoreEvaluationDriver(
            application=self.mock_application)
        with testfixtures.LogCapture():
            with six.assertRaisesRegex(
                    self,
                    RuntimeError,
                    "The number of data values returned by the MCO"):
                driver.application_started()

    def test_error_for_incorrect_output_slots(self):
        data_source_factories = \
            self.factory_registry_plugin.data_source_factories

        def run(self, *args, **kwargs):
            return [DataValue()]
        data_source_factories[0] = ProbeDataSourceFactory(
            None,
            run_function=run)
        driver = CoreEvaluationDriver(
            application=self.mock_application)
        with testfixtures.LogCapture():
            with six.assertRaisesRegex(
                    self,
                    RuntimeError,
                    "The number of data values \(1 values\)"
                    " returned by 'test_data_source' does not match"
                    " the number of output slots"):
                driver.application_started()

    def test_error_for_missing_ds_output_names(self):
        data_source_factories = \
            self.factory_registry_plugin.data_source_factories

        def run(self, *args, **kwargs):
            return [DataValue()]
        data_source_factories[0] = ProbeDataSourceFactory(
            None,
            run_function=run,
            output_slots_size=1)
        driver = CoreEvaluationDriver(
            application=self.mock_application,
        )
        with testfixtures.LogCapture():
            with six.assertRaisesRegex(
                    self,
                    RuntimeError,
                    "The number of data values \(1 values\)"
                    " returned by 'test_data_source' does not match"
                    " the number of user-defined names"):
                driver.application_started()

    def test_error_for_incorrect_kpic_output_slots(self):
        kpi_calculator_factories = \
            self.factory_registry_plugin.kpi_calculator_factories

        def run(self, *args, **kwargs):
            return [DataValue()]
        kpi_calculator_factories[0] = ProbeKPICalculatorFactory(
            None,
            run_function=run)
        driver = CoreEvaluationDriver(
            application=self.mock_application,
        )
        with testfixtures.LogCapture():
            with six.assertRaisesRegex(
                    self,
                    RuntimeError,
                    "The number of data values \(1 values\)"
                    " returned by 'test_kpi_calculator' does not match"
                    " the number of output slots"):

                driver.application_started()

    def test_error_for_missing_kpic_output_names(self):
        kpi_calculator_factories = \
            self.factory_registry_plugin.kpi_calculator_factories

        def run(self, *args, **kwargs):
            return [DataValue()]
        kpi_calculator_factories[0] = ProbeKPICalculatorFactory(
            None,
            run_function=run,
            output_slots_size=1)
        driver = CoreEvaluationDriver(
            application=self.mock_application,
        )

        with testfixtures.LogCapture():
            with six.assertRaisesRegex(
                    self,
                    RuntimeError,
                    "The number of data values \(1 values\)"
                    " returned by 'test_kpi_calculator' does not match"
                    " the number of user-defined names"):
                driver.application_started()

    def test_bind_data_values(self):
        data_values = [
            DataValue(name="foo"),
            DataValue(name="bar"),
            DataValue(name="baz")
        ]

        slot_map = (
            InputSlotMap(name="baz"),
            InputSlotMap(name="bar")
        )

        slots = (
            Slot(),
            Slot()
        )

        result = _bind_data_values(data_values, slot_map, slots)
        self.assertEqual(result[0], data_values[2])
        self.assertEqual(result[1], data_values[1])

        # Check the errors. Only one slot map for two slots.
        slot_map = (
            InputSlotMap(name="baz"),
        )

        with testfixtures.LogCapture():
            with six.assertRaisesRegex(
                    self,
                    RuntimeError,
                    "The length of the slots is not equal to the length of"
                    " the slot map"):
                _bind_data_values(data_values, slot_map, slots)

        # missing value in the given data values.
        slot_map = (
            InputSlotMap(name="blap"),
            InputSlotMap(name="bar")
        )

        with testfixtures.LogCapture():
            with six.assertRaisesRegex(
                    self,
                    RuntimeError,
                    "Unable to find requested name 'blap' in available"
                    " data values."):
                _bind_data_values(data_values, slot_map, slots)

    def test_compute_layer_results(self):
        data_values = [
            DataValue(name="foo"),
            DataValue(name="bar"),
            DataValue(name="baz"),
            DataValue(name="quux")
        ]

        def run(self, *args, **kwargs):
            return [DataValue(value=1), DataValue(value=2), DataValue(value=3)]
        ds_factory = ProbeDataSourceFactory(
            None,
            input_slots_size=2,
            output_slots_size=3,
            run_function=run)
        evaluator_model = ds_factory.create_model()

        evaluator_model.input_slot_maps = [
            InputSlotMap(name="foo"),
            InputSlotMap(name="quux")
        ]
        evaluator_model.output_slot_names = ["one", "", "three"]

        res = _compute_layer_results(
            data_values,
            [evaluator_model],
            "create_data_source"
        )
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].name, "one")
        self.assertEqual(res[0].value, 1)
        self.assertEqual(res[1].name, "three")
        self.assertEqual(res[1].value, 3)

    def test_empty_slot_name_skips_data_value(self):
        """Checks if leaving a slot name empty will skip the data value
        in the final output
        """
