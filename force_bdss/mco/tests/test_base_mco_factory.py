import unittest

from traits.trait_errors import TraitError

from force_bdss.mco.base_mco_factory import BaseMCOFactory
from force_bdss.mco.tests.test_base_mco import DummyMCO
from force_bdss.mco.tests.test_base_mco_communicator import (
    DummyMCOCommunicator,
)
from force_bdss.tests.dummy_classes.mco import (
    DummyMCOFactory,
    DummyMCOModel,
    DummyMCOParameterFactory,
)


class MCOFactory(BaseMCOFactory):
    def get_identifier(self):
        return "dummy_mco_2"

    def get_name(self):
        return "Dummy MCO 2"

    def get_model_class(self):
        return DummyMCOModel

    def get_communicator_class(self):
        return DummyMCOCommunicator

    def get_optimizer_class(self):
        return DummyMCO

    def get_parameter_factory_classes(self):
        return [DummyMCOParameterFactory]


class TestBaseMCOFactory(unittest.TestCase):
    def setUp(self):
        self.plugin = {"id": "pid", "name": "Plugin"}

    def test_initialization(self):
        factory = DummyMCOFactory(self.plugin)
        self.assertEqual(factory.id, "pid.factory.dummy_mco")
        self.assertEqual(factory.name, "Dummy MCO")
        self.assertIsInstance(factory.create_optimizer(), DummyMCO)
        self.assertIsInstance(
            factory.create_communicator(), DummyMCOCommunicator
        )
        self.assertIsInstance(factory.create_model(), DummyMCOModel)

    def test_base_object_parameter_factories(self):
        factory = MCOFactory(self.plugin)
        self.assertEqual(1, len(factory.parameter_factories))
        for parameter_factory in factory.parameter_factories:
            self.assertIsInstance(parameter_factory, DummyMCOParameterFactory)

        self.assertRaisesRegex(
            KeyError,
            "not a valid id",
            factory.parameter_factory_by_id,
            "not a valid id",
        )
        self.assertIs(
            factory.parameter_factory_by_id(factory.parameter_factories[0].id),
            factory.parameter_factories[0],
        )

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
