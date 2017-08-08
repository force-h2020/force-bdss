import unittest
from traits.api import List

from envisage.application import Application

from force_bdss.factory_registry_plugin import FactoryRegistryPlugin
from force_bdss.cli.tests.test_execution import cd

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.core_evaluation_driver import CoreEvaluationDriver
from force_bdss.core_plugins.dummy.dummy_plugin import DummyPlugin
from force_bdss.tests import fixtures


class DummyFactoryRegistryPlugin(FactoryRegistryPlugin):
    mco_factories = List()
    kpi_calculator_factories = List()
    data_source_factories = List()


def mock_factory_registry_plugin():
    plugin = DummyPlugin()
    factory_registry_plugin = DummyFactoryRegistryPlugin()
    factory_registry_plugin.mco_factories = plugin.mco_factories
    factory_registry_plugin.kpi_calculator_factories = \
        plugin.kpi_calculator_factories
    factory_registry_plugin.data_source_factories = \
        plugin.data_source_factories
    return factory_registry_plugin


class TestDirectExecution(unittest.TestCase):
    def setUp(self):
        self.mock_factory_registry_plugin = mock_factory_registry_plugin()
        application = mock.Mock(spec=Application)
        application.get_plugin = mock.Mock(
            return_value=self.mock_factory_registry_plugin
        )
        application.workflow_filepath = fixtures.get("test_csv.json")
        self.mock_application = application

    def test_initialization(self):
        driver = CoreEvaluationDriver(
            application=self.mock_application,
        )
        with cd(fixtures.dirpath()), \
                mock.patch("sys.stdin") as stdin, \
                mock.patch("sys.stdout") as stdout:

            stdin.read.return_value = "1"
            driver.application_started()
            write_args = stdout.write.call_args

        self.assertEqual(write_args[0][0], "85.0")
