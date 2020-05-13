#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import unittest

from force_bdss.core.slot import Slot


class TestSlot(unittest.TestCase):
    def test_initialization(self):
        slot = Slot()
        self.assertEqual(slot.type, "")
        self.assertEqual(slot.description, "No description")
