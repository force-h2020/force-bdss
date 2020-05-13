#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import unittest
from traits.api import TraitError

from force_bdss.core.input_slot_info import InputSlotInfo


class TestDataValue(unittest.TestCase):
    def test_initialization(self):
        slotmap = InputSlotInfo()

        self.assertEqual(slotmap.source, "Environment")
        self.assertEqual(slotmap.name, "")
        with self.assertRaises(TraitError):
            slotmap.name = "000"
