import unittest

from traits.api import Float

from force_bdss.tests.probe_classes.factory_registry_plugin import \
    ProbeFactoryRegistryPlugin

from force_bdss.core.input_slot_map import InputSlotMap
from force_bdss.core.data_value import DataValue
from force_bdss.core.slot import Slot
from force_bdss.data_sources.base_data_source import BaseDataSource
from force_bdss.data_sources.base_data_source_factory import \
    BaseDataSourceFactory
from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel
from force_bdss.ids import mco_parameter_id, factory_id
from force_bdss.kpi.base_kpi_calculator import BaseKPICalculator
from force_bdss.kpi.base_kpi_calculator_factory import BaseKPICalculatorFactory
from force_bdss.kpi.base_kpi_calculator_model import BaseKPICalculatorModel
from force_bdss.mco.base_mco import BaseMCO
from force_bdss.mco.base_mco_factory import BaseMCOFactory
from force_bdss.mco.base_mco_communicator import BaseMCOCommunicator
from force_bdss.mco.base_mco_model import BaseMCOModel
from force_bdss.mco.parameters.base_mco_parameter import BaseMCOParameter
from force_bdss.mco.parameters.base_mco_parameter_factory import \
    BaseMCOParameterFactory
from force_bdss.notification_listeners.base_notification_listener import \
    BaseNotificationListener
from force_bdss.notification_listeners.base_notification_listener_factory \
    import \
    BaseNotificationListenerFactory
from force_bdss.notification_listeners.base_notification_listener_model \
    import \
    BaseNotificationListenerModel
from force_bdss.tests import fixtures

try:
    import mock
except ImportError:
    from unittest import mock

from envisage.api import Application

from force_bdss.core_evaluation_driver import CoreEvaluationDriver, \
    _bind_data_values, _compute_layer_results


class NullMCOModel(BaseMCOModel):
    pass


class NullMCO(BaseMCO):
    def run(self, model):
        pass


class RangedParameter(BaseMCOParameter):
    initial_value = Float()
    lower_bound = Float()
    upper_bound = Float()


class RangedParameterFactory(BaseMCOParameterFactory):
    id = mco_parameter_id("enthought", "null_mco", "null")
    model_class = RangedParameter


class NullMCOCommunicator(BaseMCOCommunicator):
    def send_to_mco(self, model, kpi_results):
        pass

    def receive_from_mco(self, model):
        return []


class OneDataValueMCOCommunicator(BaseMCOCommunicator):
    """A communicator that returns one single datavalue, for testing purposes.
    """
    def send_to_mco(self, model, kpi_results):
        pass

    def receive_from_mco(self, model):
        return [
            DataValue()
        ]


class NullMCOFactory(BaseMCOFactory):
    id = factory_id("enthought", "test_mco")

    def create_model(self, model_data=None):
        return NullMCOModel(self, **model_data)

    def create_communicator(self):
        return NullMCOCommunicator(self)

    def create_optimizer(self):
        return NullMCO(self)

    def parameter_factories(self):
        return []


class NullKPICalculatorModel(BaseKPICalculatorModel):
    pass


class NullKPICalculator(BaseKPICalculator):
    def run(self, model, data_source_results):
        return []

    def slots(self, model):
        return (), ()


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


class NullKPICalculatorFactory(BaseKPICalculatorFactory):
    id = factory_id("enthought", "test_kpi_calculator")
    name = "test_kpi_calculator"

    def create_model(self, model_data=None):
        return NullKPICalculatorModel(self)

    def create_kpi_calculator(self):
        return NullKPICalculator(self)


class NullDataSourceModel(BaseDataSourceModel):
    pass


class NullDataSource(BaseDataSource):
    def run(self, model, parameters):
        return []

    def slots(self, model):
        return (), ()


class BrokenOneValueDataSource(BaseDataSource):
    """Incorrect data source implementation whose run returns a data value
    but no slot was specified for it."""
    def run(self, model, parameters):
        return [DataValue()]

    def slots(self, model):
        return (), ()


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


class NullDataSourceFactory(BaseDataSourceFactory):
    id = factory_id("enthought", "test_data_source")
    name = "test_data_source"

    def create_model(self, model_data=None):
        return NullDataSourceModel(self)

    def create_data_source(self):
        return NullDataSource(self)


class NullNotificationListener(BaseNotificationListener):
    def initialize(self, model):
        pass

    def deliver(self, event):
        pass

    def finalize(self):
        pass


class NullNotificationListenerModel(BaseNotificationListenerModel):
    pass


class NullNotificationListenerFactory(BaseNotificationListenerFactory):
    id = factory_id("enthought", "null_nl")
    name = "null_nl"

    def create_listener(self):
        return NullNotificationListener(self)

    def create_model(self, model_data=None):
        return NullNotificationListenerModel(self)


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
        factory = self.factory_registry_plugin.mco_factories[0]
        with mock.patch.object(factory.__class__,
                               "create_communicator") as create_comm:
            create_comm.return_value = OneDataValueMCOCommunicator(
                factory)
            driver = CoreEvaluationDriver(
                application=self.mock_application,
            )
            with self.assertRaisesRegexp(
                    RuntimeError,
                    "The number of data values returned by the MCO"):
                driver.application_started()

    def test_error_for_incorrect_output_slots(self):
        factory = self.factory_registry_plugin.data_source_factories[0]
        with mock.patch.object(factory.__class__,
                               "create_data_source") as create_ds:
            create_ds.return_value = BrokenOneValueDataSource(factory)
            driver = CoreEvaluationDriver(
                application=self.mock_application,
            )
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
