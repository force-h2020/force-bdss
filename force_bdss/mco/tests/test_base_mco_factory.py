import unittest

from traits.trait_errors import TraitError

from force_bdss.mco.base_mco_model import BaseMCOModel
from force_bdss.mco.tests.test_base_mco import DummyMCO
from force_bdss.mco.tests.test_base_mco_communicator import \
    DummyMCOCommunicator

try:
    import mock
except ImportError:
    from unittest import mock

from envisage.plugin import Plugin

from force_bdss.mco.base_mco_factory import BaseMCOFactory


class DummyMCOFactory(BaseMCOFactory):
    def get_identifier(self):
        return "foo"

    def get_name(self):
        return "bar"

    def get_model_class(self):
        return DummyMCOModel

    def get_communicator_class(self):
        return DummyMCOCommunicator

    def get_optimizer_class(self):
        return DummyMCO

    def parameter_factories(self):
        return []


class DummyMCOModel(BaseMCOModel):
    pass


class TestBaseMCOFactory(unittest.TestCase):
    def setUp(self):
        self.plugin = mock.Mock(spec=Plugin, id="pid")

    def test_initialization(self):
        factory = DummyMCOFactory(self.plugin)
        self.assertEqual(factory.id, 'pid.factory.foo')
        self.assertEqual(factory.name, 'bar')
        self.assertIsInstance(factory.create_optimizer(),
                              DummyMCO)
        self.assertIsInstance(factory.create_communicator(),
                              DummyMCOCommunicator)
        self.assertIsInstance(factory.create_model(),
                              DummyMCOModel)

    def test_broken_get_identifier(self):
        class Broken(DummyMCOFactory):
            def get_identifier(self):
                return None

        with self.assertRaises(ValueError):
            Broken(self.plugin)

    def test_broken_get_name(self):
        class Broken(DummyMCOFactory):
            def get_name(self):
                return None

        with self.assertRaises(TraitError):
            Broken(self.plugin)

    def test_broken_get_model_class(self):
        class Broken(DummyMCOFactory):
            def get_model_class(self):
                return None

        with self.assertRaises(TraitError):
            Broken(self.plugin)

    def test_broken_get_optimiser_class(self):
        class Broken(DummyMCOFactory):
            def get_optimizer_class(self):
                return None

        with self.assertRaises(TraitError):
            Broken(self.plugin)

    def test_broken_get_communicator_class(self):
        class Broken(DummyMCOFactory):
            def get_communicator_class(self):
                return None

        with self.assertRaises(TraitError):
            Broken(self.plugin)
