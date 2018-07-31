import unittest
from testfixtures import LogCapture

from force_bdss.core.data_value import DataValue
from force_bdss.tests.probe_classes.factory_registry_plugin import \
    ProbeFactoryRegistryPlugin
from force_bdss.core_driver_events import (
    MCOStartEvent, MCOFinishEvent, MCOProgressEvent)
from force_bdss.tests import fixtures

try:
    import mock
except ImportError:
    from unittest import mock

from envisage.api import Application

from force_bdss.core_mco_driver import CoreMCODriver


def raise_exception(*args, **kwargs):
    raise Exception()


class TestCoreMCODriver(unittest.TestCase):
    def setUp(self):
        self.factory_registry_plugin = ProbeFactoryRegistryPlugin()
        application = mock.Mock(spec=Application)
        application.get_plugin = mock.Mock(
            return_value=self.factory_registry_plugin
        )
        application.workflow_filepath = fixtures.get("test_probe.json")
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
        driver._deliver_start_event()
        self.assertIsInstance(listener.deliver_call_args[0][0], MCOStartEvent)

    def test_finished_event_handling(self):
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        listener = driver.listeners[0]
        driver._deliver_finish_event()
        self.assertIsInstance(listener.deliver_call_args[0][0], MCOFinishEvent)

    def test_progress_event_handling(self):
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        listener = driver.listeners[0]
        driver.mco.notify_new_point(
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

    def test_listener_init_exception(self):
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        registry = self.factory_registry_plugin
        factory = registry.notification_listener_factories[0]
        factory.initialize_function = raise_exception
        with LogCapture() as capture:
            listeners = driver.listeners

            capture.check(
                ("force_bdss.core_mco_driver",
                 "ERROR",
                 "Failed to initialize listener with id "
                 "'force.bdss.enthought.plugin.test.v0"
                 ".factory.probe_notification_listener' in plugin "
                 "'force.bdss.enthought.plugin.test.v0'. "
                 "The listener will be dropped."))

            self.assertEqual(len(listeners), 0)

    def test_listener_delivery_exception(self):
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        listener = driver.listeners[0]
        listener.deliver_function = raise_exception
        with LogCapture() as capture:
            driver._deliver_start_event()
            self.assertTrue(listener.deliver_called)

            capture.check(
                ("force_bdss.core_mco_driver",
                 "ERROR",
                 "Exception while delivering to listener "
                 "'force.bdss.enthought.plugin.test.v0"
                 ".factory.probe_notification_listener' in plugin "
                 "'force.bdss.enthought.plugin.test.v0'. The listener will "
                 "be dropped and computation will continue."))

    def test_finalize_error(self):
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        driver.application_started()

        listener = driver.listeners[0]
        listener.finalize_function = raise_exception
        with LogCapture() as capture:
            driver.application_stopping()
            capture.check(
                ("force_bdss.core_mco_driver",
                 "ERROR",
                 "Exception while finalizing listener "
                 "'force.bdss.enthought.plugin.test.v0"
                 ".factory.probe_notification_listener' in plugin "
                 "'force.bdss.enthought.plugin.test.v0'."))

    def test_listener_creation_error(self):
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        registry = self.factory_registry_plugin
        nl_factory = registry.notification_listener_factories[0]
        nl_factory.raises_on_create_listener = True

        with LogCapture() as capture:
            with self.assertRaises(Exception):
                driver.listeners
            capture.check(('force_bdss.core_mco_driver',
                           'ERROR',
                           'Failed to create listener with id '
                           "'force.bdss.enthought.plugin.test.v0"
                           ".factory.probe_notification_listener' "
                           "in plugin 'force.bdss.enthought.plugin"
                           ".test.v0'. This may indicate a "
                           'programming error in the plugin.'),)

    def test_create_optimizer_error(self):
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        registry = self.factory_registry_plugin
        mco_factory = registry.mco_factories[0]
        mco_factory.raises_on_create_optimizer = True

        with LogCapture() as capture:
            with self.assertRaises(Exception):
                driver.mco
            capture.check(('force_bdss.core_mco_driver',
                           'ERROR',
                           'Unable to instantiate optimizer for mco '
                           "'force.bdss.enthought.plugin.test.v0"
                           ".factory.probe_mco' in plugin "
                           "'force.bdss.enthought.plugin.test.v0'. "
                           "An exception was raised. This might "
                           'indicate a programming error in the plugin.'),)

        with LogCapture() as capture:
            with self.assertRaises(SystemExit):
                driver.application_started()

    def test_mco_run_exception(self):
        def run_func(*args, **kwargs):
            raise Exception("run_func")

        driver = CoreMCODriver(
            application=self.mock_application,
        )
        registry = self.factory_registry_plugin
        mco_factory = registry.mco_factories[0]
        mco_factory.optimizer.run_function = run_func

        with LogCapture() as capture:
            with self.assertRaises(SystemExit):
                driver.application_started()
            capture.check(('force_bdss.core_mco_driver',
                           'ERROR',
                           'Method run() of MCO with id '
                           "'force.bdss.enthought.plugin.test.v0"
                           ".factory.probe_mco' from plugin "
                           "'force.bdss.enthought.plugin.test.v0'"
                           " raised exception. This might indicate "
                           'a programming error in the plugin.'),)

    def test_nonexistent_file(self):
        self.mock_application.workflow_filepath = fixtures.get(
            "test_nonexistent.json")
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        with LogCapture() as capture:
            with self.assertRaises(SystemExit):
                driver.application_started()
            capture.check(
                ('force_bdss.core_mco_driver', 'ERROR',
                 'Unable to open workflow file.'),
            )

    def test_non_valid_file(self):
        self.mock_application.workflow_filepath = fixtures.get(
            "test_null.json")
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        with LogCapture() as capture:
            with self.assertRaises(SystemExit):
                driver.application_started()
            capture.check(
                ('force_bdss.core_mco_driver',
                 'ERROR',
                 'Unable to execute workflow due to verification errors :'),
                ('force_bdss.core_mco_driver', 'ERROR',
                 'The MCO has no defined parameters'),
                ('force_bdss.core_mco_driver', 'ERROR',
                 'Missing input slot name assignment in layer 0'),
                ('force_bdss.core_mco_driver', 'ERROR',
                 'Missing output slot name assignment in layer 0'))
