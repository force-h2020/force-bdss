import unittest

from force_bdss.ids import factory_id, plugin_id


class TestIdGenerators(unittest.TestCase):
    def test_factory_id(self):
        self.assertEqual(factory_id("foo", "bar"),
                         "force.bdss.foo.factory.bar")

        for bad_entry in ["", None, "   ", "foo bar"]:
            with self.assertRaises(ValueError):
                factory_id(bad_entry, "bar")
            with self.assertRaises(ValueError):
                factory_id("foo", bad_entry)

    def test_plugin_id(self):
        self.assertEqual(plugin_id("foo", "bar"), "force.bdss.foo.plugin.bar")

        for bad_entry in ["", None, "   ", "foo bar"]:
            with self.assertRaises(ValueError):
                plugin_id(bad_entry, "bar")
            with self.assertRaises(ValueError):
                plugin_id("foo", bad_entry)
