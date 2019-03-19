import unittest

import testfixtures

from force_bdss.tests.probe_classes.factory_registry_plugin import \
    ProbeFactoryRegistryPlugin

from force_bdss.core.data_value import DataValue
from force_bdss.tests import fixtures

from unittest import mock

from envisage.api import Application

from force_bdss.core_evaluation_driver import (
    CoreEvaluationDriver
)


class TestCoreEvaluationDriver(unittest.TestCase):
    def setUp(self):
        self.registry = ProbeFactoryRegistryPlugin()
        self.plugin = self.registry.plugin
        application = mock.Mock(spec=Application)
        application.get_plugin = mock.Mock(
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
                    "The number of data values \(2 values\)"
                    " returned by 'test_data_source' does not match"
                    " the number of output slots"):
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
                    "The run method of data source test_data_source must"
                    " return a list. It returned instead <.* 'str'>. Fix"
                    " the run\(\) method to return the appropriate entity."):
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
                    "The result list returned by DataSource test_data_source"
                    " contains an entry that is not a DataValue."
                    " An entry of type <.* 'str'> was instead found"
                    " in position 0."
                    " Fix the DataSource.run\(\) method to"
                    " return the appropriate entity."):
                driver.application_started()

    def test_error_for_missing_ds_output_names(self):

        def run(self, *args, **kwargs):
            return [DataValue(), DataValue()]

        ds_factory = self.registry.data_source_factories[0]
        ds_factory.run_function = run
        ds_factory.output_slots_size = 2
        driver = CoreEvaluationDriver(
            application=self.mock_application,
        )
        with testfixtures.LogCapture():
            with self.assertRaisesRegex(
                    RuntimeError,
                    "The number of data values \(2 values\)"
                    " returned by 'test_data_source' does not match"
                    " the number of user-defined names"):
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
            with self.assertRaises(Exception):
                driver.application_started()
            capture.check(
                ('force_bdss.core_evaluation_driver', 'INFO',
                 'Creating communicator'),
                ('force_bdss.core_evaluation_driver', 'INFO',
                 'Received data from MCO: \n whatever = 1.0 (AVERAGE)'),
                ('force_bdss.core.execution', 'INFO',
                 'Computing data layer 0'),
                ('force_bdss.core.execution', 'ERROR',
                 'Unable to create data source from factory '
                 "'force.bdss.enthought.plugin.test.v0"
                 ".factory.probe_data_source' in plugin "
                 "'force.bdss.enthought.plugin.test.v0'. "
                 "This may indicate a programming error in the plugin"))
