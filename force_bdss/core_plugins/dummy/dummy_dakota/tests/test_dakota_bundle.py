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


class TestDakotaBundle(unittest.TestCase):
    def setUp(self):
        self.plugin = mock.Mock(spec=Plugin)

    def test_initialization(self):
        bundle = DummyDakotaFactory(self.plugin)
        self.assertIn("dummy_dakota", bundle.id)
        self.assertEqual(bundle.plugin, self.plugin)

    def test_create_model(self):
        bundle = DummyDakotaFactory(self.plugin)
        model = bundle.create_model({})
        self.assertIsInstance(model, DummyDakotaModel)

        model = bundle.create_model()
        self.assertIsInstance(model, DummyDakotaModel)

    def test_create_mco(self):
        bundle = DummyDakotaFactory(self.plugin)
        ds = bundle.create_optimizer()
        self.assertIsInstance(ds, DummyDakotaOptimizer)

    def test_create_communicator(self):
        bundle = DummyDakotaFactory(self.plugin)
        ds = bundle.create_optimizer()
        self.assertIsInstance(ds, DummyDakotaOptimizer)

    def test_parameter_factories(self):
        bundle = DummyDakotaFactory(self.plugin)
        self.assertNotEqual(len(bundle.parameter_factories()), 0)
