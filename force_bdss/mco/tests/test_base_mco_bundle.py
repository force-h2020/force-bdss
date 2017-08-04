import unittest

try:
    import mock
except ImportError:
    from unittest import mock

from envisage.plugin import Plugin

from force_bdss.mco.base_mco_factory import BaseMCOFactory


class DummyMCOBundle(BaseMCOFactory):
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


class TestBaseMCOBundle(unittest.TestCase):
    def test_initialization(self):
        bundle = DummyMCOBundle(mock.Mock(spec=Plugin))
        self.assertEqual(bundle.id, 'foo')
        self.assertEqual(bundle.name, 'bar')
