import unittest
from testfixtures import LogCapture

from force_bdss.core_driver_events import (
    MCOStartEvent, MCOFinishEvent, MCOProgressEvent)
from force_bdss.notification_listeners.base_notification_listener import \
    BaseNotificationListener
from force_bdss.tests import fixtures
from force_bdss.tests.test_core_evaluation_driver import \
    mock_factory_registry_plugin

try:
    import mock
except ImportError:
    from unittest import mock

from envisage.api import Application

from force_bdss.core_mco_driver import CoreMCODriver


class TestCoreMCODriver(unittest.TestCase):
    def setUp(self):
        self.mock_factory_registry_plugin = mock_factory_registry_plugin()
        application = mock.Mock(spec=Application)
        application.get_plugin = mock.Mock(
            return_value=self.mock_factory_registry_plugin
        )
        application.workflow_filepath = fixtures.get("test_null.json")
        self.mock_application = application

    def test_initialization(self):
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        driver.application_started()

    def test_stopping(self):
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        driver.application_started()
        driver.application_stopping()

    def test_listeners(self):
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        self.assertEqual(len(driver.listeners), 1)

    def test_start_event_handling(self):
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        listener = driver.listeners[0]
        mock_deliver = mock.Mock()
        listener.__dict__["deliver"] = mock_deliver
        driver.mco.started = True
        self.assertIsInstance(mock_deliver.call_args[0][0], MCOStartEvent)

    def test_finished_event_handling(self):
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        listener = driver.listeners[0]
        mock_deliver = mock.Mock()
        listener.__dict__["deliver"] = mock_deliver
        driver.mco.finished = True
        self.assertIsInstance(mock_deliver.call_args[0][0], MCOFinishEvent)

    def test_progress_event_handling(self):
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        listener = driver.listeners[0]
        mock_deliver = mock.Mock()
        listener.__dict__["deliver"] = mock_deliver
        driver.mco.new_data = {'input': (1, 2), 'output': (3, 4)}
        self.assertIsInstance(mock_deliver.call_args[0][0], MCOProgressEvent)
        self.assertEqual(mock_deliver.call_args[0][0].input, (1, 2))
        self.assertEqual(mock_deliver.call_args[0][0].output, (3, 4))

    def test_listener_init_exception(self):
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        registry = self.mock_factory_registry_plugin
        factory = registry.notification_listener_factories[0]
        mock_create_listener = mock.Mock()
        mock_listener = mock.Mock(spec=BaseNotificationListener)
        mock_create_listener.return_value = mock_listener
        mock_listener.initialize = mock.Mock()
        mock_listener.initialize.side_effect = Exception()
        factory.__dict__["create_listener"] = mock_create_listener
        with LogCapture() as capture:
            listeners = driver.listeners

            capture.check(
                ("force_bdss.core_mco_driver",
                 "ERROR",
                 "Failed to create or initialize listener with id "
                 "force.bdss.enthought.factory.null_nl: "))

            self.assertEqual(len(listeners), 0)

    def test_listener_delivery_exception(self):
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        listener = driver.listeners[0]
        mock_deliver = mock.Mock()
        listener.__dict__["deliver"] = mock_deliver
        mock_deliver.side_effect = Exception()
        with LogCapture() as capture:
            driver.mco.started = True
            self.assertTrue(mock_deliver.called)

            capture.check(
                ("force_bdss.core_mco_driver",
                 "ERROR",
                 "Exception while delivering to listener "
                 "NullNotificationListener: "))

    def test_finalize_error(self):
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        driver.application_started()

        listener = driver.listeners[0]
        mock_finalize = mock.Mock()
        listener.__dict__["finalize"] = mock_finalize
        mock_finalize.side_effect = Exception()

        with LogCapture() as capture:
            driver.application_stopping()
            capture.check(
                ("force_bdss.core_mco_driver",
                 "ERROR",
                 "Exception while finalizing listener "
                 "NullNotificationListener: "))
