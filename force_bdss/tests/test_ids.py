#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import unittest

from force_bdss.ids import factory_id, plugin_id


class TestIdGenerators(unittest.TestCase):
    def test_factory_id(self):
        self.assertEqual(factory_id("foo", "bar"),
                         "foo.factory.bar")

        for bad_entry in ["", None, "   ", "foo bar"]:
            with self.assertRaises(ValueError):
                factory_id(bad_entry, "bar")
            with self.assertRaises(ValueError):
                factory_id("foo", bad_entry)

    def test_plugin_id(self):
        self.assertEqual(plugin_id("foo", "bar", 0),
                         "force.bdss.foo.plugin.bar.v0")

        for bad_entry in ["", None, "   ", "foo bar"]:
            with self.assertRaises(ValueError):
                plugin_id(bad_entry, "bar", 0)
            with self.assertRaises(ValueError):
                plugin_id("foo", bad_entry, 0)
            with self.assertRaises(ValueError):
                plugin_id("foo", "bar", bad_entry)
