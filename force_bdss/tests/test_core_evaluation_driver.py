import unittest
from traits.api import Float, List
from force_bdss.bundle_registry_plugin import BundleRegistryPlugin
from force_bdss.core.data_value import DataValue
from force_bdss.core.slot import Slot
from force_bdss.data_sources.base_data_source import BaseDataSource
from force_bdss.data_sources.base_data_source_bundle import \
    BaseDataSourceBundle
from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel
from force_bdss.ids import mco_parameter_id, bundle_id
from force_bdss.kpi.base_kpi_calculator import BaseKPICalculator
from force_bdss.kpi.base_kpi_calculator_bundle import BaseKPICalculatorBundle
from force_bdss.kpi.base_kpi_calculator_model import BaseKPICalculatorModel
from force_bdss.mco.base_mco import BaseMCO
from force_bdss.mco.base_mco_bundle import BaseMCOBundle
from force_bdss.mco.base_mco_communicator import BaseMCOCommunicator
from force_bdss.mco.base_mco_model import BaseMCOModel
from force_bdss.mco.parameters.base_mco_parameter import BaseMCOParameter
from force_bdss.mco.parameters.base_mco_parameter_factory import \
    BaseMCOParameterFactory
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


class NullMCOBundle(BaseMCOBundle):
    id = bundle_id("enthought", "null_mco")

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


class NullKPICalculatorBundle(BaseKPICalculatorBundle):
    id = bundle_id("enthought", "null_kpic")
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


class NullDataSourceBundle(BaseDataSourceBundle):
    id = bundle_id("enthought", "null_ds")
    name = "null_ds"

    def create_model(self, model_data=None):
        return NullDataSourceModel(self)

    def create_data_source(self):
        return NullDataSource(self)


class DummyBundleRegistryPlugin(BundleRegistryPlugin):
    mco_bundles = List()
    kpi_calculator_bundles = List()
    data_source_bundles = List()


def mock_bundle_registry_plugin():
    bundle_registry_plugin = DummyBundleRegistryPlugin()
    bundle_registry_plugin.mco_bundles = [
        NullMCOBundle(bundle_registry_plugin)]
    bundle_registry_plugin.kpi_calculator_bundles = [
        NullKPICalculatorBundle(bundle_registry_plugin)]
    bundle_registry_plugin.data_source_bundles = [
        NullDataSourceBundle(bundle_registry_plugin)]
    return bundle_registry_plugin


class TestCoreEvaluationDriver(unittest.TestCase):
    def setUp(self):
        self.mock_bundle_registry_plugin = mock_bundle_registry_plugin()
        application = mock.Mock(spec=Application)
        application.get_plugin = mock.Mock(
            return_value=self.mock_bundle_registry_plugin
        )
        application.workflow_filepath = fixtures.get("test_null.json")
        self.mock_application = application

    def test_initialization(self):
        driver = CoreEvaluationDriver(
            application=self.mock_application,
        )
        driver.application_started()

    def test_error_for_non_matching_mco_parameters(self):
        bundle = self.mock_bundle_registry_plugin.mco_bundles[0]
        with mock.patch.object(bundle.__class__,
                               "create_communicator") as create_comm:
            create_comm.return_value = OneDataValueMCOCommunicator(
                bundle)
            driver = CoreEvaluationDriver(
                application=self.mock_application,
            )
            with self.assertRaisesRegexp(
                    RuntimeError,
                    "The number of data values returned by the MCO"):
                driver.application_started()

    def test_error_for_incorrect_output_slots(self):
        bundle = self.mock_bundle_registry_plugin.data_source_bundles[0]
        with mock.patch.object(bundle.__class__,
                               "create_data_source") as create_ds:
            create_ds.return_value = BrokenOneValueDataSource(bundle)
            driver = CoreEvaluationDriver(
                application=self.mock_application,
            )
            with self.assertRaisesRegexp(
                    RuntimeError,
                    "The number of data values \(1 values\)"
                    " returned by the DataSource 'null_ds' does not match"
                    " the number of output slots"):
                driver.application_started()

    def test_error_for_missing_ds_output_names(self):
        bundle = self.mock_bundle_registry_plugin.data_source_bundles[0]
        with mock.patch.object(bundle.__class__,
                               "create_data_source") as create_ds:
            create_ds.return_value = OneValueDataSource(bundle)
            driver = CoreEvaluationDriver(
                application=self.mock_application,
            )
            with self.assertRaisesRegexp(
                    RuntimeError,
                    "The number of data values \(1 values\)"
                    " returned by the DataSource 'null_ds' does not match"
                    " the number of user-defined names"):
                driver.application_started()

    def test_error_for_incorrect_kpic_output_slots(self):
        bundle = self.mock_bundle_registry_plugin.kpi_calculator_bundles[0]
        with mock.patch.object(bundle.__class__,
                               "create_kpi_calculator") as create_kpic:
            create_kpic.return_value = BrokenOneValueKPICalculator(bundle)
            driver = CoreEvaluationDriver(
                application=self.mock_application,
            )
            with self.assertRaisesRegexp(
                    RuntimeError,
                    "The number of data values \(1 values\)"
                    " returned by the KPICalculator 'null_kpic' does not match"
                    " the number of output slots"):
                driver.application_started()

    def test_error_for_missing_kpic_output_names(self):
        bundle = self.mock_bundle_registry_plugin.kpi_calculator_bundles[0]
        with mock.patch.object(bundle.__class__,
                               "create_kpi_calculator") as create_kpic:
            create_kpic.return_value = OneValueKPICalculator(bundle)
            driver = CoreEvaluationDriver(
                application=self.mock_application,
            )
            with self.assertRaisesRegexp(
                    RuntimeError,
                    "The number of data values \(1 values\)"
                    " returned by the KPICalculator 'null_kpic' does not match"
                    " the number of user-defined names"):
                driver.application_started()
