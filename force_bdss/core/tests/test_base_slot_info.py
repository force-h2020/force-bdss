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

    def test__verify_name(self):
        noname_slot_info = BaseSlotInfo(
            name='',
            type='VOLUME',
            description='A description'
        )
        errors = noname_slot_info._verify_name()
        self.assertEqual(1, len(errors))
