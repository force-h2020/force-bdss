import unittest

from unittest import mock

from envisage.plugin import Plugin

from force_bdss.core.base_factory import BaseFactory


class DummyBaseFactory(BaseFactory):

    def get_identifier(self):
        return "dummy_factory"

    def get_name(self):
        return "Dummy Factory"


class TestBaseFactory(unittest.TestCase):

    def setUp(self):
        self.plugin_id = "pid"
        self.plugin = mock.Mock(spec=Plugin, id=self.plugin_id)

    def test_initialization(self):

        # Initialisation with an Envisage Plugin argument
        factory = DummyBaseFactory(self.plugin)
        self.assertEqual(factory.id, 'pid.factory.dummy_factory')
        self.assertEqual(factory.plugin_id, 'pid')
        self.assertEqual(factory.name, 'Dummy Factory')
        self.assertEqual(factory.description, "No description available.")

        # Initialisation with a Unicode argument
        factory = DummyBaseFactory(self.plugin_id)
        self.assertEqual(factory.id, 'pid.factory.dummy_factory')
        self.assertEqual(factory.plugin_id, 'pid')
        self.assertEqual(factory.name, 'Dummy Factory')
        self.assertEqual(factory.description, "No description available.")

    def test_not_implemented_errors(self):

        with self.assertRaises(NotImplementedError):
            BaseFactory(self.plugin)

        with mock.patch('force_bdss.core.base_factory.BaseFactory'
                        '.get_identifier', return_value=None):
            with self.assertRaisesRegex(
                    NotImplementedError,
                    'get_name was not implemented in factory '
                    "<class 'force_bdss.core.base_factory.BaseFactory'>"):
                BaseFactory(self.plugin)

        with mock.patch('force_bdss.core.base_factory.BaseFactory'
                        '.get_name', return_value=''):
            with self.assertRaisesRegex(
                    NotImplementedError,
                    'get_identifier was not implemented in factory '
                    "<class 'force_bdss.core.base_factory.BaseFactory'>"):
                BaseFactory(self.plugin)
