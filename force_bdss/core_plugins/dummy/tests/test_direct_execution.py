import unittest
from traits.api import List

from envisage.application import Application

from force_bdss.bundle_registry_plugin import BundleRegistryPlugin
from force_bdss.cli.tests.test_execution import cd

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.core_evaluation_driver import CoreEvaluationDriver
from force_bdss.core_plugins.dummy.dummy_plugin import DummyPlugin
from force_bdss.tests import fixtures


class DummyBundleRegistryPlugin(BundleRegistryPlugin):
    mco_bundles = List()
    kpi_calculator_bundles = List()
    data_source_bundles = List()


def mock_bundle_registry_plugin():
    plugin = DummyPlugin()
    bundle_registry_plugin = DummyBundleRegistryPlugin()
    bundle_registry_plugin.mco_bundles = plugin.mco_bundles
    bundle_registry_plugin.kpi_calculator_bundles = \
        plugin.kpi_calculator_bundles
    bundle_registry_plugin.data_source_bundles = plugin.data_source_bundles
    return bundle_registry_plugin


class TestDirectExecution(unittest.TestCase):
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
        with cd(fixtures.dirpath()), \
                mock.patch("sys.stdin") as stdin, \
                mock.patch("sys.stdout") as stdout:

            stdin.read.return_value = "1"
            driver.application_started()
            write_args = stdout.write.call_args

        self.assertEqual(write_args[0][0], "85.0")
