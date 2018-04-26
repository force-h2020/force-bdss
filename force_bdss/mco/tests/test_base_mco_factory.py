import unittest

import testfixtures

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


class DummyMCOModel(BaseMCOModel):
    pass


class DummyMCOFactoryFast(BaseMCOFactory):
    id = "foo"

    name = "bar"

    optimizer_class = DummyMCO

    model_class = DummyMCOModel

    communicator_class = DummyMCOCommunicator


class TestBaseMCOFactory(unittest.TestCase):
    def test_initialization(self):
        factory = DummyMCOFactory(mock.Mock(spec=Plugin))
        self.assertEqual(factory.id, 'foo')
        self.assertEqual(factory.name, 'bar')

    def test_fast_definition(self):
        factory = DummyMCOFactoryFast(mock.Mock(spec=Plugin))
        self.assertIsInstance(factory.create_optimizer(),
                              DummyMCO)
        self.assertIsInstance(factory.create_communicator(),
                              DummyMCOCommunicator)
        self.assertIsInstance(factory.create_model(),
                              DummyMCOModel)

    def test_fast_definition_errors(self):
        factory = DummyMCOFactoryFast(mock.Mock(spec=Plugin))
        factory.optimizer_class = None
        factory.model_class = None
        factory.communicator_class = None

        with testfixtures.LogCapture():
            with self.assertRaises(RuntimeError):
                factory.create_optimizer()

            with self.assertRaises(RuntimeError):
                factory.create_communicator()

            with self.assertRaises(RuntimeError):
                factory.create_model()
