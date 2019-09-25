import unittest

import testfixtures

from force_bdss.tests.probe_classes.factory_registry import \
    ProbeFactoryRegistry

from force_bdss.core.data_value import DataValue
from force_bdss.tests import fixtures

from unittest import mock

from envisage.api import Application

from force_bdss.core_evaluation_driver import (
    CoreEvaluationDriver
)


class TestCoreEvaluationDriver(unittest.TestCase):
    def setUp(self):
        self.registry = ProbeFactoryRegistry()
        self.plugin = self.registry.plugin
        application = mock.Mock(spec=Application)
        application.get_service = mock.Mock(
            return_value=self.registry
        )
        application.workflow_filepath = fixtures.get("test_probe.json")
        self.mock_application = application

    def test_initialization(self):
        driver = CoreEvaluationDriver(
            application=self.mock_application,
        )
        driver.application_started()

    def test_error_for_non_matching_mco_parameters(self):
        mco_factory = self.registry.mco_factories[0]
        mco_factory.nb_output_data_values = 2
        driver = CoreEvaluationDriver(
            application=self.mock_application)
        with testfixtures.LogCapture():
            with self.assertRaisesRegex(
                    RuntimeError,
                    "The number of data values returned by the MCO"):
                driver.application_started()

    def test_error_for_incorrect_output_slots(self):

        def run(self, *args, **kwargs):
            return [DataValue(), DataValue()]
        ds_factory = self.registry.data_source_factories[0]
        ds_factory.run_function = run
        driver = CoreEvaluationDriver(application=self.mock_application)
        with testfixtures.LogCapture():
            with self.assertRaisesRegex(
                    RuntimeError,
                    r"The number of data values \(2 values\)"
                    r" returned by 'test_data_source' does not match"
                    r" the number of output slots"):
                driver.application_started()

    def test_error_for_incorrect_return_type(self):
        def run(self, *args, **kwargs):
            return "hello"
        ds_factory = self.registry.data_source_factories[0]
        ds_factory.run_function = run
        driver = CoreEvaluationDriver(application=self.mock_application)
        with testfixtures.LogCapture():
            with self.assertRaisesRegex(
                    RuntimeError,
                    r"The run method of data source test_data_source must"
                    r" return a list. It returned instead <.* 'str'>. Fix"
                    r" the run\(\) method to return the appropriate entity."):
                driver.application_started()

    def test_error_for_incorrect_data_value_entries(self):
        def run(self, *args, **kwargs):
            return ["hello"]
        ds_factory = self.registry.data_source_factories[0]
        ds_factory.run_function = run
        driver = CoreEvaluationDriver(application=self.mock_application)
        with testfixtures.LogCapture():
            with self.assertRaisesRegex(
                    RuntimeError,
                    r"The result list returned by DataSource test_data_source"
                    r" contains an entry that is not a DataValue."
                    r" An entry of type <.* 'str'> was instead found"
                    r" in position 0."
                    r" Fix the DataSource.run\(\) method to"
                    r" return the appropriate entity."):
                driver.application_started()

    def test_mco_communicator_broken(self):
        self.registry.mco_factories[0].raises_on_create_communicator = True
        driver = CoreEvaluationDriver(
            application=self.mock_application,
        )

        with testfixtures.LogCapture() as capture:
            with self.assertRaises(Exception):
                driver.application_started()
            capture.check(
                ('force_bdss.core_evaluation_driver', 'INFO',
                 'Creating communicator'),
                ("force_bdss.core_evaluation_driver",
                 "ERROR",
                 'Unable to create communicator from MCO factory '
                 "'force.bdss.enthought.plugin.test.v0"
                 ".factory.probe_mco' in plugin "
                 "'force.bdss.enthought.plugin.test.v0'. "
                 "This may indicate a programming error in the plugin"))

    def test_data_source_broken(self):
        factory = self.registry.data_source_factories[0]
        factory.raises_on_create_data_source = True
        driver = CoreEvaluationDriver(
            application=self.mock_application,
        )

        with testfixtures.LogCapture() as capture:
            with self.assertRaises(SystemExit):
                driver.application_started()
            capture.check(
                ("force_bdss.data_sources.base_data_source_model",
                 'ERROR',
                 "Unable to create data source from factory "
                 "'force.bdss.enthought.plugin.test.v0.factory"
                 ".probe_data_source', plugin 'force.bdss.enthought."
                 "plugin.test.v0'. This might indicate a  programming"
                 " error"),
                ('force_bdss.io.workflow_reader', 'ERROR',
                 'Unable to create model for DataSource '
                 'force.bdss.enthought.plugin.test.v0.factory'
                 '.probe_data_source : ProbeDataSourceFactory'
                 '.create_data_source. This is likely due to a coding '
                 'error in the plugin. Check the logs for more information.'),
                ('force_bdss.core_evaluation_driver',
                 'ERROR',
                 'Unable to open workflow file.'))
