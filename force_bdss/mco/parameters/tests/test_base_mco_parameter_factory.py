import unittest

from envisage.plugin import Plugin
from traits.trait_errors import TraitError

from force_bdss.mco.base_mco_factory import BaseMCOFactory

try:
    import mock
except ImportError:
    from unittest import mock
from traits.api import Int


from force_bdss.mco.parameters.base_mco_parameter import BaseMCOParameter
from force_bdss.mco.parameters.base_mco_parameter_factory import \
    BaseMCOParameterFactory


class DummyMCOParameter(BaseMCOParameter):
    x = Int()


class DummyMCOParameterFactory(BaseMCOParameterFactory):
    def get_identifier(self):
        return "foo"

    def get_name(self):
        return "bar"

    def get_description(self):
        return "description"

    def get_model_class(self):
        return DummyMCOParameter


class TestBaseMCOParameterFactory(unittest.TestCase):
    def setUp(self):
        self.mco_factory = mock.Mock(
            spec=BaseMCOFactory,
            plugin=mock.Mock(
                spec=Plugin,
                id="pid"
            ),
            id="mcoid"
        )

    def test_initialization(self):
        factory = DummyMCOParameterFactory(mco_factory=self.mco_factory)
        self.assertEqual(factory.id, "mcoid.parameter.foo")
        self.assertEqual(factory.name, "bar")
        self.assertEqual(factory.description, "description")
        self.assertEqual(factory.model_class, DummyMCOParameter)
        self.assertIsInstance(factory.create_model(), DummyMCOParameter)

    def test_create_model(self):
        factory = DummyMCOParameterFactory(mco_factory=self.mco_factory)
        model = factory.create_model({"x": 42})
        self.assertIsInstance(model, DummyMCOParameter)
        self.assertEqual(model.x, 42)

        model = factory.create_model()
        self.assertIsInstance(model, DummyMCOParameter)
        self.assertEqual(model.x, 0)

    def test_broken_get_identifier(self):
        class Broken(DummyMCOParameterFactory):
            def get_identifier(self):
                return None

        with self.assertRaises(ValueError):
            Broken(self.mco_factory)

    def test_broken_get_name(self):
        class Broken(DummyMCOParameterFactory):
            def get_name(self):
                return None

        with self.assertRaises(TraitError):
            Broken(self.mco_factory)

    def test_broken_get_model_class(self):
        class Broken(DummyMCOParameterFactory):
            def get_model_class(self):
                return None

        with self.assertRaises(TraitError):
            Broken(self.mco_factory)

    def test_broken_get_description(self):
        class Broken(DummyMCOParameterFactory):
            def get_description(self):
                return None

        with self.assertRaises(TraitError):
            Broken(self.mco_factory)
