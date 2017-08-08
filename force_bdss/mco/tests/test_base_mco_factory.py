import unittest

try:
    import mock
except ImportError:
    from unittest import mock

from envisage.plugin import Plugin

from force_bdss.mco.base_mco_factory import BaseMCOFactory


class DummyMCOFactory(BaseMCOFactory):
    id = "foo"

    name = "bar"

    def create_optimizer(self):
        pass

    def create_model(self, model_data=None):
        pass

    def create_communicator(self):
        pass

    def parameter_factories(self):
        return []


class TestBaseMCOFactory(unittest.TestCase):
    def test_initialization(self):
        factory = DummyMCOFactory(mock.Mock(spec=Plugin))
        self.assertEqual(factory.id, 'foo')
        self.assertEqual(factory.name, 'bar')
