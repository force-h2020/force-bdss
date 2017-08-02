import unittest
from traits.api import TraitError

from force_bdss.core.input_slot_map import InputSlotMap


class TestDataValue(unittest.TestCase):
    def test_initialization(self):
        slotmap = InputSlotMap()

        self.assertEqual(slotmap.source, "MCO")
        self.assertEqual(slotmap.name, "")
        with self.assertRaises(TraitError):
            slotmap.name = "000"
