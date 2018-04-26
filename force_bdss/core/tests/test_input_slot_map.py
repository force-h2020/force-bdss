import unittest
from traits.api import TraitError

from force_bdss.core.input_slot_map import InputSlotInfo


class TestDataValue(unittest.TestCase):
    def test_initialization(self):
        slotmap = InputSlotInfo()

        self.assertEqual(slotmap.source, "Environment")
        self.assertEqual(slotmap.name, "")
        with self.assertRaises(TraitError):
            slotmap.name = "000"
