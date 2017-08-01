import unittest

from force_bdss.core.data_value import DataValue


class TestDataValue(unittest.TestCase):
    def test_initialization(self):
        dv = DataValue()
        self.assertEqual(dv.type, "")
        self.assertEqual(dv.value, None)
        self.assertEqual(dv.accuracy, None)
        self.assertEqual(dv.quality, "AVERAGE")
