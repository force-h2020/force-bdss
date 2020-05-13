#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import unittest
from traits.api import HasStrictTraits, TraitError

from force_bdss.local_traits import Identifier, CUBAType, PositiveInt


class Traited(HasStrictTraits):
    val = Identifier()
    cuba = CUBAType()
    positive_int = PositiveInt()


class TestLocalTraits(unittest.TestCase):
    def test_identifier(self):
        c = Traited()

        for working in ["hello", "_hello", "_0", "_hello_123", "_", ""]:
            c.val = working
            self.assertEqual(c.val, working)

        for broken in ["0", None, 123, "0hello", "hi$", "hi%"]:
            with self.assertRaises(TraitError):
                c.val = broken

    def test_cuba_type(self):
        c = Traited()
        c.cuba = "PRESSURE"
        self.assertEqual(c.cuba, "PRESSURE")

    def test_positive_int(self):
        c = Traited()
        with self.assertRaises(TraitError):
            c.positive_int = 0

        with self.assertRaises(TraitError):
            c.positive_int = -1

        c.positive_int = 3
