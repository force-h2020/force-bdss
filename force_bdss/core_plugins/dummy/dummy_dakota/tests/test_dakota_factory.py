import unittest

from envisage.plugin import Plugin

from force_bdss.core_plugins.dummy.dummy_dakota.dakota_factory import \
    DummyDakotaFactory
from force_bdss.core_plugins.dummy.dummy_dakota.dakota_model import \
    DummyDakotaModel
from force_bdss.core_plugins.dummy.dummy_dakota.dakota_optimizer import \
    DummyDakotaOptimizer

try:
    import mock
except ImportError:
    from unittest import mock


class TestDakotaFactory(unittest.TestCase):
    def setUp(self):
        self.plugin = mock.Mock(spec=Plugin)

    def test_initialization(self):
        factory = DummyDakotaFactory(self.plugin)
        self.assertIn("dummy_dakota", factory.id)
        self.assertEqual(factory.plugin, self.plugin)

    def test_create_model(self):
        factory = DummyDakotaFactory(self.plugin)
        model = factory.create_model({})
        self.assertIsInstance(model, DummyDakotaModel)

        model = factory.create_model()
        self.assertIsInstance(model, DummyDakotaModel)

    def test_create_mco(self):
        factory = DummyDakotaFactory(self.plugin)
        ds = factory.create_optimizer()
        self.assertIsInstance(ds, DummyDakotaOptimizer)

    def test_create_communicator(self):
        factory = DummyDakotaFactory(self.plugin)
        ds = factory.create_optimizer()
        self.assertIsInstance(ds, DummyDakotaOptimizer)

    def test_parameter_factories(self):
        factory = DummyDakotaFactory(self.plugin)
        self.assertNotEqual(len(factory.parameter_factories()), 0)
