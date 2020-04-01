from unittest import TestCase

import testfixtures

from force_bdss.app.evaluate_operation import EvaluateOperation
from force_bdss.core.data_value import DataValue
from force_bdss.tests import fixtures
from force_bdss.tests.probe_classes.workflow_file import (
    ProbeWorkflowFile
)


class TestEvaluateOperation(TestCase):

    def setUp(self):
        self.operation = EvaluateOperation()
        self.operation.workflow_file = ProbeWorkflowFile(
            path=fixtures.get("test_probe.json")
        )
        self.operation.workflow_file.read()
        self.registry = (
            self.operation.workflow_file.reader.factory_registry
        )

    def test__init__(self):

        operation = EvaluateOperation()
        self.assertIsNone(operation.workflow_file)
        # workflow attribute delegates to workflow_file, so
        # should raise exception if not defined
        with self.assertRaises(AttributeError):
            self.assertIsNone(operation.workflow)

    def test_assign_workflow_file(self):

        operation = EvaluateOperation()
        operation.workflow_file = ProbeWorkflowFile()
        self.assertIsNone(operation.workflow)

        operation.workflow_file.path = fixtures.get("test_empty.json")
        operation.workflow_file.read()
        self.assertIsNotNone(operation.workflow)

    def test_run(self):
        with testfixtures.LogCapture() as capture:
            self.operation.run()
            capture.check(
                ('force_bdss.app.evaluate_operation',
                 'INFO', 'Creating communicator'),
                ('force_bdss.core.workflow',
                 'INFO', 'Computing data layer 0'),
                ('force_bdss.core.execution_layer',
                 'INFO',
                 'Evaluating for Data Source test_data_source'),
                ('force_bdss.core.execution_layer',
                 'INFO', 'Passed values:'),
                ('force_bdss.core.execution_layer',
                 'INFO', '0:  foo = 1.0 (AVERAGE)'),
                ('force_bdss.core.execution_layer',
                 'INFO', 'Returned values:'),
                ('force_bdss.core.execution_layer',
                 'INFO', '0:  bar = None (AVERAGE)'),
                ('force_bdss.core.workflow',
                 'INFO', 'Aggregating KPI data')
            )

    def test_run_missing_mco(self):
        # Test for missing MCO
        self.operation.workflow.mco_model = None
        with testfixtures.LogCapture() as capture:
            with (self.assertRaisesRegex(
                    RuntimeError, "Workflow file has errors"
            )):
                self.operation.run()
            capture.check(
                ('force_bdss.app.base_operation',
                 'ERROR',
                 'Unable to execute workflow due to verification errors:'),
                ('force_bdss.app.base_operation', 'ERROR',
                 'Workflow has no MCO'),
                )

    def test_run_broken_mco_communicator(self):
        # Test for broken MCO communicator
        factory = self.registry.mco_factories[0]
        factory.raises_on_create_communicator = True

        with testfixtures.LogCapture() as capture:
            self.assertFalse(self.operation.run())
            capture.check(
                ('force_bdss.app.evaluate_operation',
                 'INFO',
                 'Creating communicator'),
                ("force_bdss.app.evaluate_operation",
                 "ERROR",
                 'Unable to create communicator from MCO factory '
                 "'force.bdss.enthought.plugin.test.v0"
                 ".factory.probe_mco' in plugin "
                 "'force.bdss.enthought.plugin.test.v0'. "
                 "This may indicate a programming error in the plugin"))

    def test_error_for_non_matching_mco_parameters(self):
        # Test for missing MCO parameter
        factory = self.registry.mco_factories[0]
        self.operation.workflow.mco_model = factory.create_model()

        with testfixtures.LogCapture():
            with (self.assertRaisesRegex(
                    RuntimeError,
                    "Workflow file has errors.") or
                  self.assertRaisesRegex(
                    RuntimeError,
                    r"The number of data values returned by the MCO "
                    r"\(1 values\) does not match the number of "
                    r"parameters specified \(0 values\). This is either "
                    "a MCO plugin error or the workflow file is "
                    "corrupted.")):
                self.operation.run()

    def test_error_for_incorrect_output_slots(self):

        def probe_run(self, *args, **kwargs):
            return [DataValue(), DataValue()]

        factory = self.registry.data_source_factories[0]
        factory.run_function = probe_run

        with testfixtures.LogCapture():
            with self.assertRaisesRegex(
                    RuntimeError,
                    r"The number of data values \(2 values\)"
                    " returned by 'test_data_source' does not match"
                    " the number of output slots it specifies "
                    r"\(1 values\). This is likely a plugin error."):
                self.operation.run()

    def test_error_for_incorrect_return_type(self):

        def probe_run(self, *args, **kwargs):
            return "hello"

        factory = self.registry.data_source_factories[0]
        factory.run_function = probe_run

        with testfixtures.LogCapture():
            with self.assertRaisesRegex(
                    RuntimeError,
                    "The run method of data source "
                    "test_data_source must return a list. It "
                    r"returned instead <.* 'str'>. Fix the run\(\)"
                    " method to return the appropriate entity."):
                self.operation.run()

    def test_error_for_incorrect_data_value_entries(self):

        def probe_run(self, *args, **kwargs):
            return ["hello"]

        factory = self.registry.data_source_factories[0]
        factory.run_function = probe_run

        with testfixtures.LogCapture():
            with self.assertRaisesRegex(
                    RuntimeError,
                    "The result list returned by DataSource "
                    "test_data_source"
                    " contains an entry that is not a DataValue."
                    " An entry of type <.* 'str'> was instead found"
                    " in position 0."
                    r" Fix the DataSource.run\(\) method to"
                    " return the appropriate entity."):
                self.operation.run()

    def test_data_source_broken(self):

        factory = self.registry.data_source_factories[0]
        factory.raises_on_create_data_source = True

        with testfixtures.LogCapture() as capture:
            with self.assertRaises(Exception):
                self.operation.run()
            capture.check(
                 ('force_bdss.data_sources.base_data_source_model',
                  'ERROR',
                  'Unable to create data source from factory '
                  "'force.bdss.enthought.plugin.test.v0.factory."
                  "probe_data_source', plugin "
                  "'force.bdss.enthought.plugin.test.v0'. "
                  "This might indicate a  programming "
                  'error'))
