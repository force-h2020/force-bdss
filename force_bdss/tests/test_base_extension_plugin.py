import unittest
from unittest import mock

from force_bdss.tests.probe_classes.probe_extension_plugin import \
    ProbeExtensionPlugin


class TestBaseExtensionPlugin(unittest.TestCase):
    def test_basic_init(self):
        plugin = ProbeExtensionPlugin()
        self.assertEqual(len(plugin.data_source_factories), 1)
        self.assertEqual(len(plugin.notification_listener_factories), 1)
        self.assertEqual(len(plugin.mco_factories), 1)
        self.assertEqual(len(plugin.ui_hooks_factories), 1)
        self.assertFalse(plugin.broken)
        self.assertEqual(plugin.error_msg, "")
        self.assertEqual(plugin.error_tb, "")
        self.assertEqual(plugin.name, "Probe extension")
        self.assertEqual(plugin.version, 0)
        self.assertEqual(plugin.description, "A description")

    def test_exception(self):
        with mock.patch.object(ProbeExtensionPlugin, "get_name") \
                as mock_get_name:
            mock_get_name.side_effect = Exception("Boom")
            plugin = ProbeExtensionPlugin()

        self.assertEqual(plugin.error_msg, "Boom")
        self.assertNotEqual(plugin.error_tb, "")
        self.assertEqual(len(plugin.data_source_factories), 0)
        self.assertEqual(len(plugin.notification_listener_factories), 0)
        self.assertEqual(len(plugin.mco_factories), 0)
        self.assertEqual(len(plugin.ui_hooks_factories), 0)
        self.assertTrue(plugin.broken)
