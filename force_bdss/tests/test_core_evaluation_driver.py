import unittest
from traits.api import Float
from force_bdss.bundle_registry_plugin import BundleRegistryPlugin
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


class NullParameter(BaseMCOParameter):
    initial_value = Float()
    lower_bound = Float()
    upper_bound = Float()


class NullParameterFactory(BaseMCOParameterFactory):
    id = mco_parameter_id("enthought", "ranged")
    model_class = NullParameter


class NullMCOCommunicator(BaseMCOCommunicator):
    def send_to_mco(self, model, kpi_results):
        pass

    def receive_from_mco(self, model):
        pass


class NullMCOBundle(BaseMCOBundle):
    id = bundle_id("enthought", "dummy_dakota")

    def create_model(self, model_data=None):
        return NullMCOModel(self)

    def create_communicator(self):
        return NullMCOCommunicator(self)

    def create_optimizer(self):
        return NullMCO(self)

    def parameter_factories(self):
        return [NullParameterFactory(self)]


class NullKPICalculatorModel(BaseKPICalculatorModel):
    pass


class NullKPICalculator(BaseKPICalculator):
    def run(self, model, data_source_results):
        pass


class NullKPICalculatorBundle(BaseKPICalculatorBundle):
    def create_model(self, model_data=None):
        return NullKPICalculatorModel(self)

    def create_kpi_calculator(self):
        return NullKPICalculator(self)


class NullDataSourceModel(BaseDataSourceModel):
    pass


class NullDataSource(BaseDataSource):
    def run(self, model, parameters):
        pass


class NullDataSourceBundle(BaseDataSourceBundle):
    def create_model(self, model_data=None):
        return NullDataSourceModel(self)

    def create_data_source(self):
        return NullDataSource(self)


def mock_bundle_registry_plugin():
    bundle_registry_plugin = mock.Mock(spec=BundleRegistryPlugin)
    bundle_registry_plugin.mco_bundles = [
        NullMCOBundle(bundle_registry_plugin)]
    bundle_registry_plugin.mco_bundle_by_id = mock.Mock(
        return_value=NullMCOBundle(bundle_registry_plugin))
    bundle_registry_plugin.kpi_calculator_bundle_by_id = mock.Mock(
        return_value=NullKPICalculatorBundle(bundle_registry_plugin))
    bundle_registry_plugin.data_source_bundle_by_id = mock.Mock(
        return_value=NullDataSourceBundle(bundle_registry_plugin))
    return bundle_registry_plugin


class TestCoreEvaluationDriver(unittest.TestCase):
    def setUp(self):
        self.mock_bundle_registry_plugin = mock_bundle_registry_plugin()
        application = mock.Mock(spec=Application)
        application.get_plugin = mock.Mock(
            return_value=self.mock_bundle_registry_plugin
        )
        application.workflow_filepath = fixtures.get("test_csv.json")
        self.mock_application = application

    def test_initialization(self):
        driver = CoreEvaluationDriver(
            application=self.mock_application,
        )
        driver.application_started()
