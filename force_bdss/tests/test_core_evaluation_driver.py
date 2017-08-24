import unittest

from traits.api import Float

from force_bdss.tests.probe_classes.factory_registry_plugin import \
    ProbeFactoryRegistryPlugin
from force_bdss.tests.probe_classes.mco import (
    ProbeMCOCommunicator, ProbeMCOFactory)
from force_bdss.tests.probe_classes.data_source import (
    ProbeDataSourceFactory)


from force_bdss.core.input_slot_map import InputSlotMap
from force_bdss.core.data_value import DataValue
from force_bdss.core.slot import Slot
from force_bdss.data_sources.base_data_source import BaseDataSource
from force_bdss.data_sources.base_data_source_factory import \
    BaseDataSourceFactory
from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel
from force_bdss.ids import mco_parameter_id
from force_bdss.kpi.base_kpi_calculator import BaseKPICalculator
from force_bdss.mco.parameters.base_mco_parameter import BaseMCOParameter
from force_bdss.mco.parameters.base_mco_parameter_factory import \
    BaseMCOParameterFactory
from force_bdss.tests import fixtures

try:
    import mock
except ImportError:
    from unittest import mock

from envisage.api import Application

from force_bdss.core_evaluation_driver import CoreEvaluationDriver, \
    _bind_data_values, _compute_layer_results


class RangedParameter(BaseMCOParameter):
    initial_value = Float()
    lower_bound = Float()
    upper_bound = Float()


class RangedParameterFactory(BaseMCOParameterFactory):
    id = mco_parameter_id("enthought", "null_mco", "null")
    model_class = RangedParameter


class OneValueMCOCommunicator(ProbeMCOCommunicator):
    """A communicator that returns one single datavalue, for testing purposes.
    """
    nb_output_data_values = 1


class BrokenOneValueKPICalculator(BaseKPICalculator):
    def run(self, model, data_source_results):
        return [DataValue()]

    def slots(self, model):
        return (), ()


class OneValueKPICalculator(BaseKPICalculator):
    def run(self, model, data_source_results):
        return [DataValue()]

    def slots(self, model):
        return (), (Slot(), )


class NullDataSourceModel(BaseDataSourceModel):
    pass


class OneValueDataSource(BaseDataSource):
    """Incorrect data source implementation whose run returns a data value
    but no slot was specified for it."""
    def run(self, model, parameters):
        return [DataValue()]

    def slots(self, model):
        return (), (
            Slot(),
        )


class TwoInputsThreeOutputsDataSource(BaseDataSource):
    """Incorrect data source implementation whose run returns a data value
    but no slot was specified for it."""
    def run(self, model, parameters):
        return [DataValue(value=1), DataValue(value=2), DataValue(value=3)]

    def slots(self, model):
        return (
            (Slot(), Slot()),
            (Slot(), Slot(), Slot())
        )


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
            communicator_class=OneValueMCOCommunicator)
        driver = CoreEvaluationDriver(
            application=self.mock_application)
        with self.assertRaisesRegexp(
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
        with self.assertRaisesRegexp(
                RuntimeError,
                "The number of data values \(1 values\)"
                " returned by 'test_data_source' does not match"
                " the number of output slots"):
            driver.application_started()

    def test_error_for_missing_ds_output_names(self):
        factory = self.factory_registry_plugin.data_source_factories[0]
        with mock.patch.object(factory.__class__,
                               "create_data_source") as create_ds:
            create_ds.return_value = OneValueDataSource(factory)
            driver = CoreEvaluationDriver(
                application=self.mock_application,
            )
            with self.assertRaisesRegexp(
                    RuntimeError,
                    "The number of data values \(1 values\)"
                    " returned by 'test_data_source' does not match"
                    " the number of user-defined names"):
                driver.application_started()

    def test_error_for_incorrect_kpic_output_slots(self):
        factory = self.factory_registry_plugin.kpi_calculator_factories[0]
        with mock.patch.object(factory.__class__,
                               "create_kpi_calculator") as create_kpic:
            create_kpic.return_value = BrokenOneValueKPICalculator(factory)
            driver = CoreEvaluationDriver(
                application=self.mock_application,
            )
            with self.assertRaisesRegexp(
                    RuntimeError,
                    "The number of data values \(1 values\)"
                    " returned by 'test_kpi_calculator' does not match"
                    " the number of output slots"):
                driver.application_started()

    def test_error_for_missing_kpic_output_names(self):
        factory = self.factory_registry_plugin.kpi_calculator_factories[0]
        with mock.patch.object(factory.__class__,
                               "create_kpi_calculator") as create_kpic:
            create_kpic.return_value = OneValueKPICalculator(factory)
            driver = CoreEvaluationDriver(
                application=self.mock_application,
            )
            with self.assertRaisesRegexp(
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

        with self.assertRaisesRegexp(
                RuntimeError,
                "The length of the slots is not equal to the length of"
                " the slot map"):
            _bind_data_values(data_values, slot_map, slots)

        # missing value in the given data values.
        slot_map = (
            InputSlotMap(name="blap"),
            InputSlotMap(name="bar")
        )

        with self.assertRaisesRegexp(
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

        mock_ds_factory = mock.Mock(spec=BaseDataSourceFactory)
        mock_ds_factory.name = "mock factory"
        mock_ds_factory.create_data_source.return_value = \
            TwoInputsThreeOutputsDataSource(mock_ds_factory)
        evaluator_model = NullDataSourceModel(factory=mock_ds_factory)

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
