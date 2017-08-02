import unittest
from traits.api import HasStrictTraits, TraitError

from force_bdss.local_traits import Identifier


class Traited(HasStrictTraits):
    val = Identifier()


class TestLocalTraits(unittest.TestCase):
    def test_identifier(self):
        c = Traited()

        for working in ["hello", "_hello", "_0", "_hello_123", "_", ""]:
            c.val = working
            self.assertEqual(c.val, working)

        for broken in ["0", None, 123, "0hello", "hi$", "hi%"]:
            with self.assertRaises(TraitError):
                c.val = broken
