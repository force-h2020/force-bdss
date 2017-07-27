import unittest

from force_bdss.ids import bundle_id, plugin_id


class TestIdGenerators(unittest.TestCase):
    def test_bundle_id(self):
        self.assertEqual(bundle_id("foo", "bar"),
                         "force.bdss.bundle.foo.bar")

        for bad_entry in ["", None, "   ", "foo bar"]:
            with self.assertRaises(ValueError):
                bundle_id(bad_entry, "bar")
            with self.assertRaises(ValueError):
                bundle_id("foo", bad_entry)

    def test_plugin_id(self):
        self.assertEqual(plugin_id("foo", "bar"), "force.bdss.plugin.foo.bar")

        for bad_entry in ["", None, "   ", "foo bar"]:
            with self.assertRaises(ValueError):
                plugin_id(bad_entry, "bar")
            with self.assertRaises(ValueError):
                plugin_id("foo", bad_entry)
