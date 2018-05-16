import unittest

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
        self.assertEqual(plugin.error, "")
