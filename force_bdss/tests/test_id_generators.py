import unittest

from force_bdss.id_generators import bundle_id


class TestIdGenerators(unittest.TestCase):
    def test_bundle_id(self):
        self.assertEqual(bundle_id("foo", "bar"),
                         "force.bdss.bundles.foo.bar")

        for bad_entry in ["", None, "   ", "foo bar"]:
            with self.assertRaises(ValueError):
                bundle_id(bad_entry, "bar")
            with self.assertRaises(ValueError):
                bundle_id("foo", bad_entry)
