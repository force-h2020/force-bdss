import unittest
from testfixtures import LogCapture

from force_bdss.mco.events import MCOStartEvent
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

    def test_event_handling(self):
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        listener = driver.listeners[0]
        mock_deliver = mock.Mock()
        listener.__dict__["deliver"] = mock_deliver
        event = MCOStartEvent()
        driver.mco.event = event
        self.assertTrue(mock_deliver.call_args[0][0], event)

    def test_listener_initialization_exception(self):
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        listener = driver.listeners[0]
        mock_deliver = mock.Mock()
        listener.__dict__["deliver"] = mock_deliver
        mock_deliver.side_effect = Exception()
        with LogCapture() as capture:
            driver.mco.event = MCOStartEvent()
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
