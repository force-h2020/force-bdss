#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import unittest

from force_bdss.core.data_value import DataValue


class TestDataValue(unittest.TestCase):
    def test_initialization(self):
        dv = DataValue()
        self.assertEqual(dv.type, "")
        self.assertEqual(dv.value, None)
        self.assertEqual(dv.accuracy, None)
        self.assertEqual(dv.quality, "AVERAGE")

    def test_string(self):
        dv = DataValue(type="PRESSURE", name="p1", value=10)
        self.assertEqual(str(dv), "PRESSURE p1 = 10 (AVERAGE)")
        dv = DataValue(type="PRESSURE",
                       name="p1",
                       value=10,
                       accuracy=0.1,
                       quality="POOR")
        self.assertEqual(str(dv), "PRESSURE p1 = 10 +/- 0.1 (POOR)")
