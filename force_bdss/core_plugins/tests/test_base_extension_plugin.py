#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import unittest
import testfixtures
from unittest import mock

from force_bdss.tests.probe_classes.probe_extension_plugin import \
    ProbeExtensionPlugin


class TestBaseExtensionPlugin(unittest.TestCase):
    def test_basic_init(self):
        plugin = ProbeExtensionPlugin()
        self.assertEqual(1, len(plugin.data_source_factories))
        self.assertEqual(1, len(plugin.notification_listener_factories))
        self.assertEqual(1, len(plugin.mco_factories))
        self.assertEqual(1, len(plugin.ui_hooks_factories))
        self.assertFalse(plugin.broken)
        self.assertEqual("", plugin.error_msg)
        self.assertEqual("", plugin.error_tb)
        self.assertEqual("Probe extension", plugin.name)
        self.assertEqual(0, plugin.version)
        self.assertEqual("A description", plugin.description)

    def test_exception(self):
        with mock.patch.object(ProbeExtensionPlugin, "get_name") \
                as mock_get_name, \
                testfixtures.LogCapture():
            mock_get_name.side_effect = Exception("Boom")
            plugin = ProbeExtensionPlugin()

        self.assertEqual(plugin.error_msg, "Boom")
        self.assertNotEqual(plugin.error_tb, "")
        self.assertEqual(0, len(plugin.data_source_factories))
        self.assertEqual(0, len(plugin.notification_listener_factories))
        self.assertEqual(0, len(plugin.mco_factories))
        self.assertEqual(0, len(plugin.ui_hooks_factories))
        self.assertTrue(plugin.broken)
