from unittest import TestCase, mock

import testfixtures

from force_bdss.app.optimize_operation import OptimizeOperation
from force_bdss.core.data_value import DataValue
from force_bdss.events.mco_events import (
    MCOProgressEvent,
)
from force_bdss.mco.base_mco import BaseMCO
from force_bdss.tests import fixtures
from force_bdss.tests.probe_classes.workflow_file import ProbeWorkflowFile
from force_bdss.tests.probe_classes.notification_listener import (
    ProbeUIEventNotificationListener)


class TestOptimizeOperation(TestCase):
    def setUp(self):
        self.operation = OptimizeOperation()
        self.operation.workflow_file = ProbeWorkflowFile(
            path=fixtures.get("test_probe.json")
        )
        self.operation.workflow_file.read()
        self.registry = self.operation.workflow_file.reader.factory_registry

    def test__init__(self):

        operation = OptimizeOperation()
        self.assertEqual([], operation.listeners)

        self.assertIsNone(operation.workflow_file)
        # workflow attribute delegates to workflow_file, so
        # should raise exception if not defined
        with self.assertRaises(AttributeError):
            self.assertIsNone(operation.workflow)

    def test_assign_workflow_file(self):

        operation = OptimizeOperation()
        operation.workflow_file = ProbeWorkflowFile()
        self.assertIsNone(operation.workflow)

        operation.workflow_file.path = fixtures.get("test_empty.json")
        operation.workflow_file.read()
        self.assertIsNotNone(operation.workflow)

    def test__set_threading_events(self):
        factory = self.registry.notification_listener_factories[0]
        factory.listener_class = ProbeUIEventNotificationListener
        listener = factory.create_listener()

        self.operation._set_threading_events(listener)
        self.assertIs(self.operation._pause_event,
                      listener._pause_event)
        self.assertIs(self.operation._stop_event,
                      listener._stop_event)

    def test_create_mco(self):

        # Test normal operation
        mco = self.operation.create_mco()
        self.assertIsInstance(mco, BaseMCO)

        # Now cause an exception to occur when BaseMCO is
        # created
        mco_factory = self.registry.mco_factories[0]
        mco_factory.raises_on_create_optimizer = True

        with testfixtures.LogCapture() as capture:
            with self.assertRaises(Exception):
                self.operation.create_mco()
            capture.check(
                (
                    "force_bdss.app.optimize_operation",
                    "ERROR",
                    "Unable to instantiate optimizer for mco "
                    "'force.bdss.enthought.plugin.test.v0"
                    ".factory.probe_mco' in plugin "
                    "'force.bdss.enthought.plugin.test.v0'. "
                    "An exception was raised. This might "
                    "indicate a programming error in the plugin.",
                )
            )

    def test_mco_run_exception(self):
        def run_func(*args, **kwargs):
            raise Exception("run_func")

        # Cause an exception to occur when BaseMCO is
        # run
        mco_factory = self.registry.mco_factories[0]
        mco_factory.optimizer.run_function = run_func

        with testfixtures.LogCapture() as capture:
            with self.assertRaises(Exception):
                self.operation.run()
            capture.check(
                (
                    "force_bdss.app.optimize_operation",
                    "ERROR",
                    "Method run() of MCO with id "
                    "'force.bdss.enthought.plugin.test.v0"
                    ".factory.probe_mco' from plugin "
                    "'force.bdss.enthought.plugin.test.v0'"
                    " raised exception. This might indicate "
                    "a programming error in the plugin.",
                )
            )

    def test_progress_event_handling(self):

        self.operation._initialize_listeners()
        listener = self.operation.listeners[0]

        self.operation.workflow.mco_model.notify_progress_event(
            [DataValue(value=1), DataValue(value=2)],
            [DataValue(value=3), DataValue(value=4)],
        )

        self.assertIsInstance(
            listener.deliver_call_args[0][0], MCOProgressEvent
        )

        event = listener.deliver_call_args[0][0]

        self.assertEqual(1, event.optimal_point[0].value, 1)
        self.assertEqual(2, event.optimal_point[1].value, 2)
        self.assertEqual(3, event.optimal_kpis[0].value, 3)
        self.assertEqual(4, event.optimal_kpis[1].value, 4)

    def test_terminating_workflow(self):
        self.operation._stop_event.set()
        self.operation._initialize_listeners()
        with mock.patch(
            "force_bdss.app.optimize_operation.OptimizeOperation"
            "._finalize_listeners"
        ) as mock_call:
            with self.assertRaisesRegex(SystemExit, "BDSS stopped"):
                self.operation._deliver_start_event()
            mock_call.assert_called_once()

    ##############################################
    # RUN TESTS: POSSIBLY COMMON WITH EVALUATE OPERATION
    ##############################################

    def test_non_valid_file(self):

        # Provide a workflow that is invalid
        self.operation.workflow_file = ProbeWorkflowFile(
            path=fixtures.get("test_null.json")
        )
        self.operation.workflow_file.read()

        with testfixtures.LogCapture() as capture:
            with self.assertRaises(RuntimeError):
                self.operation.run()
            capture.check(
                (
                    "force_bdss.app.base_operation",
                    "ERROR",
                    "Unable to execute workflow due to verification errors:"
                ),
                (
                    "force_bdss.app.base_operation",
                    "ERROR",
                    "The MCO has no defined parameters"
                ),
                (
                    "force_bdss.app.base_operation",
                    "ERROR",
                    "The MCO has no defined KPIs"
                ),
                (
                    "force_bdss.app.base_operation",
                    "ERROR",
                    "The number of input slots (1 values) returned by "
                    "'test_data_source' does "
                    'not match the number of user-defined names specified '
                    '(0 values). This is '
                    'either a plugin error or a file error.'
                ),
                (
                    'force_bdss.app.base_operation',
                    'ERROR',
                    "The number of output slots (1 values) returned by "
                    "'test_data_source' does "
                    'not match the number of user-defined names specified '
                    '(0 values). This is '
                    'either a plugin error or a file error.')
            )

    def test_run_empty_workflow(self):
        # Load a blank workflow
        self.operation.workflow_file = ProbeWorkflowFile(
            path=fixtures.get("test_empty.json")
        )
        self.operation.workflow_file.read()

        with testfixtures.LogCapture() as capture:
            with self.assertRaises(RuntimeError):
                self.operation.run()
            capture.check(
                (
                    "force_bdss.app.base_operation",
                    "ERROR",
                    "Unable to execute workflow due to verification errors:"
                ),
                (
                    "force_bdss.app.base_operation",
                    "ERROR",
                    "Workflow has no MCO"
                ),
                (
                    "force_bdss.app.base_operation",
                    "ERROR",
                    "Workflow has no execution layers"
                )
            )

    def test_run_missing_mco(self):
        # Test for missing MCO
        self.operation.workflow.mco_model = None
        with testfixtures.LogCapture() as capture:
            with self.assertRaisesRegex(
                RuntimeError, "Workflow file has errors"
            ):
                self.operation.run()
            capture.check(
                (
                    "force_bdss.app.base_operation",
                    "ERROR",
                    "Unable to execute workflow due to verification errors:"
                ),
                (
                    "force_bdss.app.base_operation",
                    "ERROR",
                    "Workflow has no MCO"
                )
            )
