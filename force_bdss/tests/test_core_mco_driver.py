import unittest

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

    def test_listeners(self):
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        self.assertEqual(len(driver.listeners), 1)

    def test_event_handling(self):
        driver = CoreMCODriver(
            application=self.mock_application,
        )
        driver.mco.event = MCOStartEvent()
