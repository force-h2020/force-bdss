import unittest
from xxlimited import Null

from traits.api import Float, List
from force_bdss.factory_registry_plugin import FactoryRegistryPlugin
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

from force_bdss.core_evaluation_driver import CoreEvaluationDriver


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
    id = factory_id("enthought", "null_mco")

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
    id = factory_id("enthought", "null_kpic")
    name = "null_kpic"

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


class NullDataSourceFactory(BaseDataSourceFactory):
    id = factory_id("enthought", "null_ds")
    name = "null_ds"

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


class DummyFactoryRegistryPlugin(FactoryRegistryPlugin):
    mco_factories = List()
    kpi_calculator_factories = List()
    data_source_factories = List()
    notification_listener_factories = List()


def mock_factory_registry_plugin():
    factory_registry_plugin = DummyFactoryRegistryPlugin()
    factory_registry_plugin.mco_factories = [
        NullMCOFactory(factory_registry_plugin)]
    factory_registry_plugin.kpi_calculator_factories = [
        NullKPICalculatorFactory(factory_registry_plugin)]
    factory_registry_plugin.data_source_factories = [
        NullDataSourceFactory(factory_registry_plugin)]
    factory_registry_plugin.notification_listener_factories = [
        NullNotificationListenerFactory(factory_registry_plugin)
    ]
    return factory_registry_plugin


class TestCoreEvaluationDriver(unittest.TestCase):
    def setUp(self):
        self.mock_factory_registry_plugin = mock_factory_registry_plugin()
        application = mock.Mock(spec=Application)
        application.get_plugin = mock.Mock(
            return_value=self.mock_factory_registry_plugin
        )
        application.workflow_filepath = fixtures.get("test_null.json")
        self.mock_application = application

    def test_initialization(self):
        driver = CoreEvaluationDriver(
            application=self.mock_application,
        )
        driver.application_started()

    def test_error_for_non_matching_mco_parameters(self):
        factory = self.mock_factory_registry_plugin.mco_factories[0]
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
        factory = self.mock_factory_registry_plugin.data_source_factories[0]
        with mock.patch.object(factory.__class__,
                               "create_data_source") as create_ds:
            create_ds.return_value = BrokenOneValueDataSource(factory)
            driver = CoreEvaluationDriver(
                application=self.mock_application,
            )
            with self.assertRaisesRegexp(
                    RuntimeError,
                    "The number of data values \(1 values\)"
                    " returned by 'null_ds' does not match"
                    " the number of output slots"):
                driver.application_started()

    def test_error_for_missing_ds_output_names(self):
        factory = self.mock_factory_registry_plugin.data_source_factories[0]
        with mock.patch.object(factory.__class__,
                               "create_data_source") as create_ds:
            create_ds.return_value = OneValueDataSource(factory)
            driver = CoreEvaluationDriver(
                application=self.mock_application,
            )
            with self.assertRaisesRegexp(
                    RuntimeError,
                    "The number of data values \(1 values\)"
                    " returned by 'null_ds' does not match"
                    " the number of user-defined names"):
                driver.application_started()

    def test_error_for_incorrect_kpic_output_slots(self):
        factory = self.mock_factory_registry_plugin.kpi_calculator_factories[0]
        with mock.patch.object(factory.__class__,
                               "create_kpi_calculator") as create_kpic:
            create_kpic.return_value = BrokenOneValueKPICalculator(factory)
            driver = CoreEvaluationDriver(
                application=self.mock_application,
            )
            with self.assertRaisesRegexp(
                    RuntimeError,
                    "The number of data values \(1 values\)"
                    " returned by 'null_kpic' does not match"
                    " the number of output slots"):
                driver.application_started()

    def test_error_for_missing_kpic_output_names(self):
        factory = self.mock_factory_registry_plugin.kpi_calculator_factories[0]
        with mock.patch.object(factory.__class__,
                               "create_kpi_calculator") as create_kpic:
            create_kpic.return_value = OneValueKPICalculator(factory)
            driver = CoreEvaluationDriver(
                application=self.mock_application,
            )
            with self.assertRaisesRegexp(
                    RuntimeError,
                    "The number of data values \(1 values\)"
                    " returned by 'null_kpic' does not match"
                    " the number of user-defined names"):
                driver.application_started()
