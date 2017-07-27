import unittest

from force_bdss.mco.base_mco_bundle import BaseMCOBundle


class DummyMCOBundle(BaseMCOBundle):
    id = "foo"

    name = "bar"

    def create_optimizer(self, application, model):
        pass

    def create_model(self, model_data=None):
        pass

    def create_communicator(self, application, model):
        pass


class TestBaseMCOBundle(unittest.TestCase):
    def test_initialization(self):
        bundle = DummyMCOBundle()
        self.assertEqual(bundle.id, 'foo')
        self.assertEqual(bundle.name, 'bar')
