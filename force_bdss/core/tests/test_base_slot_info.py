import unittest

from force_bdss.core.base_slot_info import BaseSlotInfo


class TestBaseSlotInfo(unittest.TestCase):

    def setUp(self):

        self.slot_info = BaseSlotInfo(
            name='Some_variable',
            type='VOLUME',
            description='A description'
        )

    def test_getstate(self):
        self.assertDictEqual(
            {'name': 'Some_variable',
             'type': 'VOLUME',
             'description': 'A description'},
            self.slot_info.__getstate__()
        )
