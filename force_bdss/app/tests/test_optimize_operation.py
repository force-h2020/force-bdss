from unittest import TestCase

import testfixtures

from force_bdss.app.optimize_operation import OptimizeOperation
from force_bdss.core.data_value import DataValue
from force_bdss.core_driver_events import (
    MCOStartEvent, MCOFinishEvent, MCOProgressEvent)
from force_bdss.mco.base_mco import BaseMCO
from force_bdss.tests import fixtures
from force_bdss.tests.probe_classes.workflow_file import (
    ProbeWorkflowFile
)


def raise_exception(*args, **kwargs):
    raise Exception()


class TestOptimizeOperation(TestCase):

    def setUp(self):
        self.operation = OptimizeOperation()
        self.operation.workflow_file = ProbeWorkflowFile(
            path=fixtures.get("test_probe.json")
        )
        self.operation.workflow_file.read()
        self.registry = (
            self.operation.workflow_file.reader.factory_registry
        )

    def test__init__(self):

        operation = OptimizeOperation()
        self.assertIsNone(operation.mco)
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

    def test_run_missing_mco(self):
        # Test for missing MCO
        self.operation.workflow.mco_model = None
        with testfixtures.LogCapture() as capture:
            with self.assertRaisesRegex(
                    RuntimeError,
                    "Workflow file has errors"):
                self.operation.run()
            capture.check(
                ('force_bdss.app.optimize_operation',
                 'ERROR',
                 'Unable to execute workflow due to verification errors:'),
                ('force_bdss.app.optimize_operation',
                 'ERROR',
                 'Workflow has no MCO'),
            )

    def test__initialize_listeners(self):

        # Test normal operation
        self.operation._initialize_listeners()
        self.assertEqual(1, len(self.operation.listeners))
        self.assertTrue(self.operation.listeners[0].initialize_called)

        # Test for error on creation of listener, we expect
        # an Exception and log message
        factory = self.registry.notification_listener_factories[0]
        factory.raises_on_create_listener = True

        with testfixtures.LogCapture() as capture:
            with self.assertRaises(Exception):
                self.operation._initialize_listeners()
            capture.check(
                ("force_bdss.app.optimize_operation",
                 "ERROR",
                 "Failed to create listener with id "
                 "'force.bdss.enthought.plugin.test.v0"
                 ".factory.probe_notification_listener' in plugin "
                 "'force.bdss.enthought.plugin.test.v0'. "
                 "This may indicate a programming error in the "
                 "plugin."))

        # Test for error on initialization of listener, we
        # only expect a log message
        factory.raises_on_create_listener = False
        factory.raises_on_initialize_listener = True

        with testfixtures.LogCapture() as capture:
            self.operation._initialize_listeners()
            capture.check(
                ("force_bdss.app.optimize_operation",
                 "ERROR",
                 "Failed to initialize listener with id "
                 "'force.bdss.enthought.plugin.test.v0"
                 ".factory.probe_notification_listener' in plugin "
                 "'force.bdss.enthought.plugin.test.v0'. "
                 "The listener will be dropped."))

    def test__finalize_listeners(self):

        # Test normal operation
        self.operation._initialize_listeners()
        listener = self.operation.listeners[0]
        self.operation._finalize_listeners()

        self.assertEqual(0, len(self.operation.listeners))
        self.assertTrue(listener.finalize_called)

        # Now initialise a set of listeners that will raise an
        # exception when finalized to test error handling
        factory = self.registry.notification_listener_factories[0]
        factory.raises_on_finalize_listener = True

        self.operation._initialize_listeners()
        listener = self.operation.listeners[0]

        with testfixtures.LogCapture() as capture:
            self.operation._finalize_listeners()
            capture.check(
                ("force_bdss.app.optimize_operation",
                 "ERROR",
                 "Exception while finalizing listener "
                 "'force.bdss.enthought.plugin.test.v0"
                 ".factory.probe_notification_listener' in plugin "
                 "'force.bdss.enthought.plugin.test.v0'."))

        self.assertEqual(0, len(self.operation.listeners))
        self.assertTrue(listener.finalize_called)

    def test_deliver_listeners(self):
        # Test normal operation
        self.operation._initialize_listeners()
        listener = self.operation.listeners[0]

        # Deliver a start event
        self.operation._deliver_start_event()
        self.assertTrue(listener.deliver_called)
        self.assertIsInstance(
            listener.deliver_call_args[0][0],
            MCOStartEvent
        )

        # Deliver a finish event
        self.operation._deliver_finish_event()
        self.assertIsInstance(
            listener.deliver_call_args[0][0],
            MCOFinishEvent
        )

        # Now initialise a set of listeners that will raise an
        # exception when delivered to test error handling
        factory = self.registry.notification_listener_factories[0]
        factory.raises_on_deliver_listener = True

        self.operation._initialize_listeners()
        listener = self.operation.listeners[0]

        with testfixtures.LogCapture() as capture:
            self.operation._deliver_start_event()
            self.assertTrue(listener.deliver_called)
            capture.check(
                ("force_bdss.app.optimize_operation",
                 "ERROR",
                 "Exception while delivering to listener "
                 "'force.bdss.enthought.plugin.test.v0"
                 ".factory.probe_notification_listener' in plugin "
                 "'force.bdss.enthought.plugin.test.v0'. "
                 "The listener will be dropped and computation "
                 "will continue."))

    def test_create_mco(self):

        # Test normal operation
        self.assertIsNone(self.operation.mco)
        self.operation.create_mco()
        self.assertIsInstance(self.operation.mco, BaseMCO)

        # Now cause an exception to occur when BaseMCO is
        # created
        mco_factory = self.registry.mco_factories[0]
        mco_factory.raises_on_create_optimizer = True

        with testfixtures.LogCapture() as capture:
            with self.assertRaises(Exception):
                self.operation.create_mco()
            capture.check(
                ('force_bdss.app.optimize_operation',
                 'ERROR',
                 'Unable to instantiate optimizer for mco '
                 "'force.bdss.enthought.plugin.test.v0"
                 ".factory.probe_mco' in plugin "
                 "'force.bdss.enthought.plugin.test.v0'. "
                 "An exception was raised. This might "
                 'indicate a programming error in the plugin.')
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
                ('force_bdss.app.optimize_operation',
                 'ERROR',
                 'Method run() of MCO with id '
                 "'force.bdss.enthought.plugin.test.v0"
                 ".factory.probe_mco' from plugin "
                 "'force.bdss.enthought.plugin.test.v0'"
                 " raised exception. This might indicate "
                 'a programming error in the plugin.')
            )

    def test_progress_event_handling(self):

        self.operation.create_mco()
        listener = self.operation.listeners[0]
        self.operation.mco.notify_new_point(
            [DataValue(value=1), DataValue(value=2)],
            [DataValue(value=3), DataValue(value=4)],
            [0.5, 0.5])
        self.assertIsInstance(
            listener.deliver_call_args[0][0],
            MCOProgressEvent)

        event = listener.deliver_call_args[0][0]

        self.assertEqual(event.optimal_point[0].value, 1)
        self.assertEqual(event.optimal_point[1].value, 2)
        self.assertEqual(event.optimal_kpis[0].value, 3)
        self.assertEqual(event.optimal_kpis[1].value, 4)
        self.assertEqual(event.weights[0], 0.5)
        self.assertEqual(event.weights[0], 0.5)

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
                ('force_bdss.app.optimize_operation',
                 'ERROR',
                 'Unable to execute workflow due to verification errors:'),
                ('force_bdss.app.optimize_operation',
                 'ERROR', 'Workflow has no MCO'),
                ('force_bdss.app.optimize_operation',
                 'ERROR',
                 'Workflow has no execution layers')
            )

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
                ('force_bdss.app.optimize_operation',
                 'ERROR',
                 'Unable to execute workflow due to verification errors:'),
                ('force_bdss.app.optimize_operation',
                 'ERROR',
                 'The MCO has no defined parameters'),
                ('force_bdss.app.optimize_operation',
                 'ERROR',
                 'The MCO has no defined KPIs'),
                ('force_bdss.app.optimize_operation',
                 'ERROR',
                 'An Input Slot variable has an undefined name'),
                ('force_bdss.app.optimize_operation',
                 'ERROR',
                 'All output variables have undefined names.'),
                ('force_bdss.app.optimize_operation',
                 'ERROR',
                 'An Output Slot variable has an undefined name'))
