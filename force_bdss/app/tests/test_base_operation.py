#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from unittest import TestCase, mock

import testfixtures

from force_bdss.app.base_operation import BaseOperation
from force_bdss.tests import fixtures
from force_bdss.tests.probe_classes.workflow_file import (
    ProbeWorkflowFile
)
from force_bdss.tests.probe_classes.notification_listener import (
    ProbeUIEventNotificationListener)
from force_bdss.events.mco_events import (
    MCOStartEvent,
    MCOFinishEvent
)


class TestBaseOperation(TestCase):

    def setUp(self):
        self.operation = BaseOperation()
        self.operation.workflow_file = ProbeWorkflowFile(
            path=fixtures.get("test_probe.json")
        )
        self.operation.workflow_file.read()
        self.registry = (
            self.operation.workflow_file.reader.factory_registry
        )

    def test__init__(self):

        operation = BaseOperation()
        self.assertIsNone(operation.workflow_file)
        # workflow attribute delegates to workflow_file, so
        # should raise exception if not defined
        with self.assertRaises(AttributeError):
            self.assertIsNone(operation.workflow)

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
                (
                    "force_bdss.app.base_operation",
                    "ERROR",
                    "Failed to create listener with id "
                    "'force.bdss.enthought.plugin.test.v0"
                    ".factory.probe_notification_listener' in plugin "
                    "'force.bdss.enthought.plugin.test.v0'. "
                    "This may indicate a programming error in the "
                    "plugin.",
                )
            )

        # Test for error on initialization of listener, we
        # only expect a log message
        factory.raises_on_create_listener = False
        factory.raises_on_initialize_listener = True

        with testfixtures.LogCapture() as capture:
            self.operation._initialize_listeners()
            capture.check(
                (
                    "force_bdss.app.base_operation",
                    "ERROR",
                    "Failed to initialize listener with id "
                    "'force.bdss.enthought.plugin.test.v0"
                    ".factory.probe_notification_listener' in plugin "
                    "'force.bdss.enthought.plugin.test.v0'. "
                    "The listener will be dropped.",
                )
            )

        # Test setting of stop and pause threading events on
        # a UIEventNotificationMixin listener
        factory.raises_on_initialize_listener = False

        with mock.patch(
                'force_bdss.app.optimize_operation.OptimizeOperation'
                '._set_threading_events') as mock_set_thread:
            self.operation._initialize_listeners()
            self.assertEqual(0, mock_set_thread.call_count)

            factory.listener_class = ProbeUIEventNotificationListener
            self.operation._initialize_listeners()
            self.assertEqual(0, mock_set_thread.call_count)

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
                (
                    "force_bdss.app.base_operation",
                    "ERROR",
                    "Exception while finalizing listener "
                    "'force.bdss.enthought.plugin.test.v0"
                    ".factory.probe_notification_listener' in plugin "
                    "'force.bdss.enthought.plugin.test.v0'.",
                )
            )

        self.assertEqual(0, len(self.operation.listeners))
        self.assertTrue(listener.finalize_called)

    def test_deliver_listeners(self):
        # Test normal operation
        self.operation._initialize_listeners()
        listener = self.operation.listeners[0]

        # Deliver a start event
        self.operation._deliver_start_event()
        self.assertTrue(listener.deliver_called)
        self.assertIsInstance(listener.deliver_call_args[0][0], MCOStartEvent)

        # Deliver a finish event
        self.operation._deliver_finish_event()
        self.assertIsInstance(listener.deliver_call_args[0][0], MCOFinishEvent)

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
                (
                    "force_bdss.app.base_operation",
                    "ERROR",
                    "Exception while delivering to listener "
                    "'force.bdss.enthought.plugin.test.v0"
                    ".factory.probe_notification_listener' in plugin "
                    "'force.bdss.enthought.plugin.test.v0'. "
                    "The listener will be dropped and computation "
                    "will continue.",
                )
            )
